
search_config = [

            {'name': 'hostname__contains','title':'主机名','type':'input'},
            {'name': 'cabinet_num', 'title': "机柜号", 'type': 'input'},
            {'name': 'server_status_id', 'title': '服务器状态', 'type': 'select', 'choice_name': 'status_choices'},

        ]

table_config = [
            {
                'q': None,
                "display": True,
                'title': '选择',
                'text': {'tpl':'<input type="checkbox" value="{nid}" />','kwargs':{'nid': '@id' }},
                'attr':{'class':'c1','nid':'@id'},

            },
            {
                'q': 'id',
                "display": False,
                'title': 'ID',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
                'attr': {},
            },
            {
                'q': 'hostname',
                "display": True,
                'title': '主机名',
                'text': {'tpl': '{a1}','kwargs':{'a1': '@hostname'}},
                'attr': {'class': 'c1','edit':'true','origin':'@hostname','name':'hostname'},
            },
            {
                'q': 'sn',
                'title': '序列号',
                "display": True,
                'text': {'tpl': '{a1}','kwargs':{'a1': '@sn'}},
                'attr': {'class': 'c1','edit':'true','origin':"@sn",'name':'sn'},
            },
            {
                'q': 'os_platform',
                'title': '系统',
                "display": True,
                'text': {'tpl': '{a1}','kwargs':{'a1': '@os_platform'}},
                'attr': {'class': 'c1','edit':'true','origin':'@os_platform','name':'os_platform'},
            },
            {
                'q': 'os_version',
                "display": True,
                'title': '系统版本',
                'text': {'tpl': '{a1}','kwargs':{'a1': '@os_version'}},
                'attr': {'class': 'c1'},
            },
            {
                'q': 'business_unit__name',
                "display": True,
                'title': '业务线',
                'text': {'tpl': '{a1}','kwargs':{'a1': '@business_unit__name'}},
                'attr': {'class': 'c1'},
            },
            {
                'q': 'server_status_id',
                "display": True,
                'title': '服务器状态',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
                'attr': {'class': 'c1','edit':'true','edit-type':'select','choice-key':'status_choices','origin':'@server_status_id','name':'server_status_id'},
            },
            {
                'q': None,
                "display": True,
                'title': '操作',
                'text': {'tpl': '<a href="/edit/{nid}/">编辑</a> | <a href="/del/{uid}/">删除</a> ', 'kwargs': {'nid': '@id','uid': '@id'}},
                'attr': {},
            },
        ]