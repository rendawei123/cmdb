# cmdb服务器资产管理系统

### 为什么要设计这个系统

原来是使用excel来维护服务器资产，搭载samb服务，多个运维人员效率很低，可信度低

搭建运维自动话平台很麻烦

因此有必要开发自动话管理系统

### 目标

1. 服务器资产自动采集
2. 报表
3. 提供API（接口）：给其他软件或系统提供数据

### 设计思路

1. 服务器资产自动采集：设计硬件系统自动采集的软件，安装给每个服务器，然后使其每天执行一次进行采集数据，然后筛选过滤出有用的信息，通过python代码发送post请求，将信息发送给Django程序提供的API通过request模块实现发送
2. 写个Django程序，为所有自动采集数据的软件提供API，让采集软件将信息汇总到Django程序，然后存入数据库，然后还可以提供给别人用
3. 写后台管理：对数据库进行怎删改查，提供数据管理

### 资产采集

资产采集就是通过shell命令获取服务器相关信息，然后取得字符串结果，然后发送

使用的技术：

* shell命令，解析
* request模块，使用代码来实现发送http强求
* 高度可扩展，可插拔式，参考Django源码中的中间件来实现
* 配置文件，为了让用户使用方便，将默认配置文件，放在内部，只让用户做常用配置
* 继承、传参方式兼容三种采集方式
* traceback

#### 问题1:扩展

需要获得的资产信息很多，基本使用shell命令来提取，不能一条一条的执行，可扩展性很差，效率不高

解决：

创建src文件夹里面创建plugin文件夹，专门存放内存、网卡等采集信息文件，然后在主函数中直接调用这些方法就行了，需要用哪个调用那个，这样可扩展行就很强了

知识点：

类的基本用法

#### 问题2：可插拔

我们为了怎加可扩展性而创建了很多的插件来分开处理，这样，但是如何让主函数灵活的调用这些插件

解决：

参考Django配置的设计思路，添加专门的配置文件，之后，如果需要添加或删除哪一个插件，直接在配置文件中进行修改，大大降低了配置的操作难度

知识点：

* 源码的配置方法


* 根据字符串导入模块，将字符串分解成真实的路径和方法 

  ```python
  import importlib
  v = 'src.plungins.nic.Nic'

  path, class_name = rsplit('.',maxsplit=1)
  m = importlib.import_module(path)   #m就是导入的模块

  cls = getattr(m,'Nic') # cls就是m模块下面的类
  obj = cls()   # 实例化，
  obj.process()   # 执行process方法，得到返回值
  ```

#### 问题3:配置文件

现在需要的插件可以在配置文件里面配置了，但是，我门自己有很多的配置，用户也可以自己配置，用户也可以修改你原本的配置，如何处理好这些配置之间的关系呢？

解决：

参考Django源码的配置文件，我们可以定义两个配置文件，一个是本身的配置，一个是提供给用户进行自定一的配置，在读取配置的时候，先读本身的配置，然后再读用户配置，如果用户配置和本身配置重合的话，就会覆盖默认配置

知识点：

* 类的call方法的合理利用

* 类的静态方法

* init文件是在导入模块名的时候执行，所以直接在这个文件里面获取用户配置和默认配置

* 导入模块

  ```python
  import importlib
  ```

* 反射：获取global_settings里面的值，

  ```python
  #  获取global_settings里面的变量名和值
  for item in dir(global_settings):
  	if item.isupper():
        print(item, getattr(global_setting,item))
  ```

* 模块多次导入时只会使用一个对象，叫做单例模式

* 设置环境变量

  ```python
  os.environ['AUTO_CLIENT_SETTINGS'] = 'conf.settings'
  # 当进程运行起来的时候可以设置键值对为AUTO_CLIENT_SETTINGS和conf.settings，用这种方法来取用户配置信息
  ```

#### 问题4:兼容性

现在我们有三种数据采集模式，一种是agent模式，一种是ssh模式，还有一种是第三方工具，我们希望我们写的软件三种方式都能兼容，只是通过修改配置文件来完成

解决；

* 鉴于每一个插件都要执行这三种模式，我们可以定义一个父类，在父类上面写好所有的三种采集模式，然后让插件继承这个类即可
* 利用传参的方式，通过传入函数名的方法来执行函数
* 注意，不同的方式传如服务器的IP以及可以让用户配置的参数问题
* 过程中还要输出错误信息，使用try。。。except
* 使用抽象类，来保证类里面必须要有配置好的方法

知识点：

* 类的继承
* 大批量服务器进行API数据同时上传问题

#### 问题5:如何捕捉错误信息

解决：

错误捕捉

```python
import traceback

try:
  ...
except Exception as e:
  print(traceback.format_exc())
```

### API

软件将资产采集到之后就涉及到讲资产信息通过API汇报给主机，主机得到数据后，会讲数据存储到数据库，还会通过API讲数据提供给别人使用，每次请求过来之后，我门线判断数据库里面有没有信息，没有就创建，有了就判断、比较、更新、记录日志等处理。

使用的技术：

get获取，post发送，以及线程池，orm，数据库操作的问题

#### 问题1：如何发送数据

当我门使用request.post 发送的时候，系统默认是按照form表单中的k1=1&k2=2 这种类型发送的，而这种发送方式是需要content-type:application/x-www-form-urlencoded来识别，这种方式是发不了字典格式的，即使发送字典，也会只把字典中的key取出来发送

解决：

给request定义请求头

```python
request.post(self.api, json=server_dict)
# 这句活做了两件事情，首先实现字段序列化，其次实现自带请求头，content-type:application/json
```

在接受数据的时候使用reuqest.body来取，并且是字节类型，就直接是字典格式

```python
server_dict = json.loads(request.body.decode('utf-8'))
```

知识点：

* request请求发送的方式
* ajax请求发送的方式
* form请求发送的方式

#### 问题2：多台服务器传输效率

那么多服务器，同时向主机提供的API汇报数据的话，如果是串行的，岂不是很慢

解决：

通过python线程池模块给每一个agent软件开线程，让他们同时向主机API传输数据

知识点：

* 线程池

```python
from concurrent.futures import ThreadPoolExecutor
pool = ProcessPoolExecutor(10)  # 开10个线程
pool.submit(task,i)    # 运行线程，括号里面分别为函数名和参数
```

* 线程池

#### 问题3：数据库创建

我们的server端通过API获取数据后需要保存到数据库，但是不仅API需要用到数据库，后台管理程序也同样需要数据库，那这个数据库到底要保存在那里呢？

解答：

由于数据库两个程序都要调用，并且很频繁，我们直接再创建一个app，专门来使用数据库，这样，不仅可扩展性高，并且管理清晰

知识点：

* 数据库操作
* ORM查找

#### 问题4：资产入库

如何处理资产存入数据库，资产变更等，并且产生报表

解答：

资产入库直接根据orm写入数据即可，但是需要做个判断，是否已经存在，如果存在，再继续判断是否有变更，如果有变更就需要讲变更前后的数据统计出来，然后将数据库中的内容进行update更新，如果没有的话存入数据库，这样就可以统计出资产的变化等内容。

在资产入库这边，也是基于Django配置文件，实现可插拔式操作，这样就显得很有条理

知识点：

* 集合

* 数据库

* ORM

* 反射

  ```
  hasattr()
  getattr()
  setattr()
  ```

#### 问题5：如何获取今日未采集资产以及上架和下架服务器

我们采集资产都是分批量采集，这样，服务器就有可能某一天没采集到，这样我们就应该知道今日哪些服务器没有采集资源，有些服务器还没有上架或者已经下架的服务器也要记录

解决：

在数据库设计中添加采集资源当天的日期字段、以及状态信息（上架、下架、离线等），也就是说，在资产入库的那天自动更新为当天的日期，这样每天运行的时候可以根据这个字段判断当天有没有采集，状态也是一样

#### 问题6：API验证

我们在使用API提交或者获取数据的时候有可能被别人获取，并且进行获取数据和提交数据，如何进行有效的验证来避免吗？

解决：

参考tonado源码

1. 在维护一个key，这个key两端都有，自定义一个请求头，header={'auth-api':key}发送给主机，然后主机在request的header里面找到key然后对比，如果和自己的key一样的话，验证成功，

   >  注意，在自定义请求头的时候字母和字母之间用-链接，不能用下划线
   >
   >  主机取到的值为   request.META里面取到{"HTTP_AUTH_API": key}

2. 但是，这样的话请求头别人照样可以拿到，我们可以让这个key动态起来，也就是和时间配合，使用md5加密，将加密后的结果以及当时的时间添加到请求头中发送过去，然后主机里面有key，再加上请求头里面发送过来的时间同样进行md5，如果一样的话，就验证成功，

3. 但是如果这样的话我门会生成很多的被攻击的加密值，我门应该在服务端添加时间显示，比如10秒，在10秒以内的可以验证成功，在10秒意外的就不允许

4. 但是还是有问题，如果别人在很快的时间内获取API然后进行操作的话，还是挡不住，因此我门需要在服务端维护一个列表或者字典，如果一个请求访问过的话记录下来，如果下次又有一样的话，就拒绝访问

### 后台管理（curd）插件

*后台管理基本上就是对数据库的一些怎删改查*



# 服务器

### 服务器

 *服务器其实就是一台更牛逼的电脑*

初创公司

租云服务器、买服务器（买服务器需要很大成本的维护）----装系统--------租公网IP-------------租域名---------------------建立公网IP和域名之间的关系

大型公司

买服务器------------租机房----------------维护人员

超大型公司

买服务器---------------建机房----------------运维

### 管理系统（自动化运维平台）

- 自动装系统
- 配置管理系统
  - 装什么软件
  - 装什么版本
- 监控系统
- 代码发布系统
  - rsync
  - git/svn
  - 比特流
- 服务器的管理

  ​	服务器资产自动采集

  	报表

  	数据交换

### SaltStack

> 关闭防火墙以及se

```
"""
1. 安装salt-master
    yum install salt-master
2. 修改配置文件：/etc/salt/master
    interface: 0.0.0.0    # 表示Master的IP 
3. 启动
    service salt-master start
"""
```

master : service salt-master start

```
"""
1. 安装salt-minion
    yum install salt-minion

2. 修改配置文件 /etc/salt/minion
    master: 10.211.55.4           # master的地址
    或
    master:
        - 10.211.55.4
        - 10.211.55.5
    random_master: True

    id: c2.salt.com                    # 客户端在salt-master中显示的唯一ID
3. 启动
    service salt-minion start
"""
```

授权

```
"""
salt-key -L                    # 查看已授权和未授权的slave
salt-key -a  salve_id      # 接受指定id的salve
salt-key -r  salve_id      # 拒绝指定id的salve
salt-key -d  salve_id      # 删除指定id的salve
"""
```

执行命令

在master服务器上对salve进行远程操作

```
salt 'c2.salt.com' cmd.run  'ifconfig'


import salt.client
local = salt.client.LocalClient()
result = local.cmd('c2.salt.com', 'cmd.run', ['ifconfig'])
```

官网

1. Run the following commands to install the SaltStack repository and key:

   ```
   sudo yum install https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm 
   ```

2. Run `sudo yum clean expire-cache`

3. Install the salt-minion, salt-master, or other Salt components:

   - `sudo yum install salt-master`
   - `sudo yum install salt-minion`



# 软件部署

```
- 服务器管理回顾
- 问题？
- 坑，SN号唯一
	- 物理机，SN唯一
	- 虚拟机，sn相同的
	规则，约束：主机名
- 事务：
	某些行为组合成一个原子性操作；
	回滚；
	条件：
		数据库：innodb
		  代码：事务
- 数据库补充

- 后台管理
```

内容详细：

```
1. 服务器管理回顾
	- 资产采集
		- 线程池
		- 兼容三种方式
		- 可插拔式插件
		- 配置文件
		- requests
			发送：
				requests.post(url='',data=,json=)
				requests.get()
			Django接受：
				request.POST, content-type:
		- traceback
		- paramiko模块，基于SSH链接远程主机并执行命令
		- SaltStack
		- API验证
			key,time|time
	- API
	- 后台管理
2. 问题？
	a. 服务器资产采集系统流程？
		  ssh：中控机，
		 salt：master，
		agent：每台服务器都需要
	
	b. 代码如何部署到服务器上？
		- git
		- 代码打成：rpm包，运维
			yum install xxxxx
			
	c. 什么时候安装到服务器上的？
		服务器装完系统后，自动做环境初始化:c1.com
			puppet 模板
			
				c1.com 文件：
					yum install python
					yum isntall requests
					create file a1.py
					cp xx  xxx 
					yum install xxxxx
					加入到定时任务中
				c2.com 
					yum install python
					yum isntall requests
					create file a1.py
					cp xx  xxx 
					
			saltstack 模块
				c1.com 文件：
					yum install python
					yum isntall requests
					create file a1.py
					cp xx  xxx 
					yum install xxxxx
				c2.com 
					yum install python
					yum isntall requests
					create file a1.py
					cp xx  xxx 
	d. 如何运行：
		Salt和SSH：
			Linux写定时任务，执行bin目录下可执行文件
			- 获取未采集主机名（用户手动通过后台管理录入）
			- 采集数据
			- 汇报API
		Agent：
			Linux写定时任务，执行bin目录下可执行文件
			- Agent上执行，采集资产并自动汇报
			- 数据库有：更新
			- 数据库无：增加【自动发现】
		
		**** 主机名不能重复 ****
```

```
梳理：
	a. 程序开发，完成
	b. 部署：
		    Agent模式，部署到每台机器【什么时候？如何部署？定时任务】
		SSH和Salt模式，部署到中控机【什么时候？如何部署？定时任务】，
			前提：
				手动：IDC运维，装机前登录服务器管理系统，找到指定机器，修改主机名；
				 API：通过Http请求进行操作
```

```
3. sn号唯一 & 如何实现允许临时修改主机名
	物理机：
		sn，物理机唯一
		
		详细：
			后台管理：
				买服务器，清单：SN号，硬盘，内存...
				作业：python 读取excel，xldt
			
			资产采集：
				sn进行比较
```

```
	物理机+虚拟机：
		hostname,前提先定义规则，主机名不允许重复
		
		Agent：
			买服务器，清单：SN号，硬盘，内存...
			资产采集：
				hostname
		SSh,salt:
			后台管理：
				买服务器，清单：SN号，硬盘，内存...，录入
				
			装机：
				c1.com 
			...
				
	问题：如果临时修改了主机名，可能会出现资产重复汇报。
		  
		  安装系统完成后，立即执行采集资产任务：
			old_hostname = cert文件空
			new_hostname = 获取当前主机名【未篡改】
			
			如果： old_hostname为空，
				   new_hostname，进行汇报并且写入到cert文件中
```

```
			old_hostname = cert文件空
			new_hostname = 获取当前主机名【未篡改】
			if old_hostname ！= new_hostname：
				old_hostname
```

```
	统一口径：
		SSH和Salt模式：
			1. 购买，厂商提供：sn，硬盘和网卡基本信息，机房，机柜以及机柜上位置。通过excel录入到数据库。
			2. 
				手动：找到指定机器，安装系统，设置主机名，安装相关软件。
				自动：cobbler装机+saltstack/puppet进行初始化
				
				后台管理：更新主机名
				
			3. 唯一标识： 主机名
		Agent： 
			物理机：
				1. 购买，厂商提供：sn，硬盘和网卡基本信息，机房 机房，机柜以及机柜上位置。通过excel录入到数据库。
				2. 
					手动：找到指定机器，安装系统，设置主机名，安装相关软件。
					自动：cobbler装机+saltstack/puppet进行初始化
				3. 唯一标识： SN
				
			物理机+虚拟机：
				1. 购买，厂商提供：sn
				2. 
					手动：找到指定机器，安装系统，设置主机名，安装相关软件。
					自动：cobbler装机+saltstack/puppet进行初始化
				3. 
					采集资产：
						- 自动发现： 自动收录硬件信息，【管理员，业务线，机房，手动操作】
						- 已经存在： 更新
					
				4. 唯一标识： 主机名

4. 事务
	- 代码
	- innodb
	
	def tran(request):
		from django.db import transaction
		try:
			with transaction.atomic():
				models.UserProfile.objects.create(name='a1',email='xxx',phone='xxxx',mobile='xxxx')
				models.Server.objects.create(hostname='uuuuu',sn='FDIJNFIK234')
		except Exception as e:
			return HttpResponse('出现错误')

		return HttpResponse('执行成功')
```





### 数据采集模式

*数据采集的基本方式是，服务器上安装有三中模式，分别为agent模式，*

#### agent模式

*agent模式，agent负责采集，采集过后发送给api进行入库处理，这种模式需要在每台机器上安装agent，然后他们分别一起汇报给总的API*

优点：速度快

缺点：缺点是每台机器都要安装agent

适用：服务器数量比较多的公司

实现（代码是放在每一台服务器上面的）

```python
# agent 模式, 代码是放在每台服务器上的
import subprocess
result = subprocess.getoutput('ifconfig')
```

#### 基于ssh模式

*服务器上不需要安装任何软件，全程靠ssh服务，但是需要一台服务器作为中控机，然后中控机分别给从每个服务器取数据，然后中控机把数据发送给API，但是速度慢*

缺点：速度慢

优点：无agent

应用：小型公司

实现(代码是放在中控机上面的)

```pyhton
# 2. SSH模式

# pip3 install paramiko
import paramiko

# ip 192.168.16.72
# 用户名 root
# 密码 redhat
#
# 用户名和密码方式
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.16.72', port=22, username='root', password='redhat')
stdin, stdout, stderr = ssh.exec_command('ifconfig')
result = stdout.read()
ssh.close()
print(result)

# 公钥私钥方式
import paramiko
# 创建ssh对象
private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 链接机器
ssh.connect(hostname='c1.salt.com', port=22, username='wupeiqi', pkey=private_key)
# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# 获取命令结果
result = stdout.read()
ssh.close()
```

#### 第三方工具（saltstack）

*第三方工具也需要每个服务器安装minion，然后需要有一台服务器安装master，然后由master控制minion，然后拿到结果传给API，它内部不是靠ssh做的，二十靠rpc模式做的，比ssh速度快，内部靠队列实现*

适用：一般公司都使用这种方式

实现（master）

```python
# import subprocess
# subprocess.getoutput('salt "c1.com" cmd.run "命令"')
```

