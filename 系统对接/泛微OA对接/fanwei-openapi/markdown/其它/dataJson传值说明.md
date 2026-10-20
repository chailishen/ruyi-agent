# dataJson传值说明

- **文档 ID**: `840723450080886785`
- **业务模块**: 其它
- **是否 API 接口**: 否（说明文档）

## 正文

## dataJson传值说明
- 单个控件传单个值{
	"dataDetails": [{
		"fieldId": "控件id",
		"fieldValue": ["控件值"]
	}]
}
- 控件传多个值{
	"dataDetails": [{
		"fieldId": "控件id",
		"fieldValue": ["选项1", "选项2", "选项3"]
	}]
}
- 明细表中的控件{
	"dataDetails": [{
		"fieldId": "控件id",
		"fieldValue": [{
			"index": 1,
			"value": ["明细表第一行控件值"]
		}, {
			"index": 2,
			"value": ["明细表第二行控件值"]
		}]
	}]
}
- 多个控件传值{
	"dataDetails": [{
		"fieldId": "控件id",
		"fieldValue": ["控件值"]
	}, {
		"fieldId": "控件id",
		"fieldValue": ["控件值"]
	}]
}
##### 第一类：文本输入框、多行文本框、单选框、下拉菜单、日期、数字输入框、金额、邮箱、电话、手机、运算控件、评分控件、进度条、身份证、地理位置
- 例1：单选框#普通布局的单选框 
{
	"dataDetails": [{
		"fieldId": "1566099556955787865",
		"fieldValue": ["选项1"]
	}]
}
#明细表中的单选框 
{
	"dataDetails": [{
		"fieldId": "1566099556955787865",
		"fieldValue": [{
			"index": 1,
			"value": ["选项1"]
		}, {
			"index": 2,
			"value": ["选项2"]
		}]
	}]
}
- 例2：日期控件#普通布局中的日期控件 
{
	"dataDetails": [{
		"fieldId": "5137302563258719042",
		"fieldValue": ["2019-11-06"]
	}]
}
#明细表中的日期控件 
{
	"dataDetails": [{
		"fieldId": "5137302563258719042",
		"fieldValue": [{
			"index": 1,
			"value": ["2019-11-06"]
		}, {
			"index": 2,
			"value": ["2019-11-16"]
		}]
	}]
}
- 例3：人员控件#普通布局中的人员控件 
{
	"dataDetails": [{
		"fieldId": "5137302564445519051",
		"fieldValue": ["巍巍"]
	}]
}
#明细表中的人员控件 
{
	"dataDetails": [{
		"fieldId": "5137302564445519051",
		"fieldValue": [{
			"index": 1,
			"value": ["巍巍"]
		}, {
			"index": 2,
			"value": ["巍巍"]
		}]
	}]
}
- 例4：多级下拉框控件{
	"dataDetails": [{
		"fieldId": "3747303343096505866",
		"fieldValue": ["选项1", "选项12", "选项122"]
	}]
}
##### 第二类：复选框、日期区间、多级下拉框、关联项目、关联任务、关联文档、关联审批、关联日程、关联表单数据、关联客户、关联线索、关联订单、客户联系人、关联商机、关联产品、关联合同、人员、部门
- 例1：复选框#普通布局中的复选框 
{
	"dataDetails": [{
		"fieldId": "5137302563258719039",
		"fieldValue": ["选项1", "选项2"]
	}]
}
#明细表中的复选框 
{
	"dataDetails": [{
		"fieldId": "5137302563258719042",
		"fieldValue": [{
			"index": 1,
			"value": ["选项1", "选项2"]
		}, {
			"index": 2,
			"value": ["选项1", "选项2", "选项3"]
		}]
	}]
}
- 例3：关联任务#普通布局中的关联任务 
{
	"dataDetails": [{
		"fieldId": "5137302567402719061",
		"fieldValue": ["任务A", "任务B"]
	}]
}
#明细表中的关联任务 
{
	"dataDetails": [{
		"fieldId": "5137302567402719061",
		"fieldValue": [{
			"index": 1,
			"value": ["任务A", "任务B"]
		}, {
			"index": 2,
			"value": ["任务C", "任务D"]
		}]
	}]
}
- 例4：日期区间
注：暂不支持：数据源、图片单选、图片多选、附件、图片、签名、电子发票、子表控件不需要传值：编号控件、分割线、描述文字，轮播控件
