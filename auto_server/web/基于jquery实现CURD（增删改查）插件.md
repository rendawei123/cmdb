### 基于jquery实现CURD（增删改查）插件

*以前的做法是首先在后台获取数据，然后在前端使用模板语言循环展示，现在我们应该写成插件形式直接写成一个文件，在view里面专门去进行配置，而不用修改原代码，然后通过引入就可以实现功能。前后端分离。*

### 数据如何传送到前端

后端：

```python
from django.http import JsonResponse

def server_json(request):
	server_list = models.Server.objects.values(*values)[page_obj.start:page_obj.end]
    response = {
        'data_list': list(server_list),
    }
    return JsonResponse(response)
```

前端接收

```html
$.ajax({
            url:requestUrl,
            type: 'GET',
            data: {'pageNum':pageNum},
            dataType: 'JSON',
            success:function (response) {
				console.log(response.data_list)
        })
```

> 注意：
>
> 1. 为了防止插件传参冲突，在制作成插件的时候使用自执行函数
>
> ```javascript
> (function(arg){....})()
> ```
>
> 2. 为了方便扩展以及定义何时执行，应该使用jquery扩展
>
> ```javascript
> // 定义扩展
> jq.extend({
>         "nBList":function (url) {
>             requestUrl = url;
>             init(1);
>             bindSearchConditionEvent();
>         },
>     });
>
> // 调用
> $(function () {
>         $.nBList("/server_json.html");
>     })
> ```
>
> 

### 获得数据如何知道显示哪些内容以及怎么显示

在后台通过配置文件来规定获取哪些数据以及怎么显示，然后以字典的方式将这些信息返回给前端，前端取得数据之后使用jquery生成标签，然后显示在页面上，这样，以后要修改显示的内容什么的就可以直接修改配置文件就行了

> 注意：
>
> 1. 我们使用jquery在前端生成页面的时候在执行函数前必须要清空，不然如果多执行一次，会继续创建标签，着不是我们想要的
> 2. 循环的时候容易乱
> 3. 这样写的话加载比较慢，因此我们需要在加载的时候播放效果，让用户知道我们正在加载中
> 4. 显示配置的时候如果不想显示内容，想显示标签的话，应该取None，但是必须在取值函数前判断一下
> 5. 合理利用字符串格式化定制特定的内容@什么的

### 如何在数据库中查询但是不在页面上面显示

我们可以在配置文件中定义哪些内容不需要在页面上显示，然后和数据一起以字典的方式发送给前端，前端收到之后每次在制作标签的时候首先进行判断，如果为true的话显示，否则不去制作标签

### 如何显示下拉框这种形式

我门在页面上面生成了各种标签后，我门就需要显示下拉框的内容，要取内容，就要获得他的id，而且不能显示，而且如果遇到choice这种形式，如何显示他的中文

如果在model里面有这种choice

```python
server_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )
server_status_id = models.IntegerField(choices=server_status_choices, default=1)
```

如何让它在前端显示中文呢：

使用模板语言实现

```python
def xxxxx(server_list):
    # [{},{}]
    for row in server_list:
        for item in models.Server.server_status_choices:
            if item[0] ==  row['server_status_id']:
                row['server_status_id_name'] = item[1]
                break
        yield row

        
def test(request):
    """
    赠送，模板语言显示choice
    :param request:
    :return:
    """
    # server_list = models.Server.objects.all()
    # for row in server_list:
    #     print(row.id,row.hostname,row.business_unit.name,"===",row.server_status_id,row.get_server_status_id_display() )

    # server_list = models.Server.objects.all().values('hostname','server_status_id')
    # for row in server_list:
    #     for item in models.Server.server_status_choices:
    #         if item[0] ==  row['server_status_id']:
    #             row['server_status_id_name'] = item[1]
    #             break

    data_list = models.Server.objects.all().values('hostname', 'server_status_id')

    return render(request,'test.html',{'server_list':xxxxx(data_list)})
  
# 前端获取
{% for row in server_list %}
        <li>
            {{ row.hostname }} = {{ row.server_status_id_name }}
        </li>
{% endfor %}


```

如果要写成插件应该怎么做呢

* 首先配置好id然后发送给前端


* 首先将所有的choice发送给前端

```python
response = {
        'global_choices_dict':{
            'status_choices': models.Server.server_status_choices
        },
    }
```

* 前端获取值

```javascript
var GLOBAL_CHOICES_DICT = {
        // 'status_choices': [[0,'xxx'],]
        // 'xxxx_choices': [[0,'xxx'],]
    };

// 处理数据
GLOBAL_CHOICES_DICT = response.global_choices_dict;

// 然后循环遍历，获取ID为配置里面ID的对应的值
```



要点：

1. 正则表达式字符串格式化实现

```
name.replace(/a/g,function(k,v){console.log(k,v);return 'b'})
```

2. 给字符串添加方法

   ```
   String.propotype.方法 = function(){};
   ```

### 定制属性

如果需要给标签定制属性，原理一样，将属性在配置文件中写好，然后发送给前端，然后在前端创建标签的时候将属性setattr添加到标签即可

> 注意，后台的标签不同，应该进行一个判断和切割

### 分页

* 首先需要前端发送给后端页码的数据（第几页）
* 后台获取页码之后，按照以前写分页的方式写
* 计算总个数，查询数据，使用Django页码模块进行分页
* 和之前写的分页不同的是，以前写的分页是使用a标签，现在改成点击页码让他执行一次函数

```javascript
        for i in range(pager_start, pager_end):
            if i == self.current_page:
                tpl = ' <li class="active"><a onclick="$.changePage(%s)"  >%s</a></li>' % (i,i,)
            else:
                tpl = ' <li><a onclick="$.changePage(%s)" >%s</a></li>' % (i, i,)
            page_list.append(tpl)
```

### 组合搜索

搜索条件配置

* 将搜索条件等配置写到配置文件中，然后发送给前端显示

下拉框

* 读取需要的信息，
* 创建下拉框标签
* 给下拉框绑定时间，点击后修改母框内容，同时修改后面的input框内容，生成那种标签，都需要判断
* 如何记住当前的状态，不让每次都初始化：给标签添加属性
* 记住前端状态，然后发送给后台页面

如何发送给后台搜索条件

* 直接找到标签的值发送给后台，后台需要接受然后进行数据筛选
* 如果同样的内容搜索条件不一样，应该使用列表来保存他们，而发送列表就需要补充  conditional = True
* 发送字典类型记得    JSON.stringify(condition) 来发送

合理使用Q

知识点：

父级塌陷：class = clearfix

### 进入编辑模式

本质上就是把文本变成input框，退出时变回文本

ajax发送问题

```javascript
$.ajax({
  url: requestUrl,
  type: 'PUT',
  data: JSON.stringify(update_dict),
  traditional: true,
  dataType: 'JSON',
  success: function (arg) {
  }
})
```

csrf_token问题

```javascript
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // 请求头中设置一次csrf-token
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                // xhr.setRequestHeader("X-CSRFToken", 'csrftoken');
            }
        }
    })
```

发送forbidden问题

使用装饰器

```python
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def server_json(request):
```



 

