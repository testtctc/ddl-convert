# encoding=utf-8
import re
from ddl.parse import ColumnsExtract

COLDEF= re.compile("""(`?\w+`?)\s+(\w+).*?(comment\s+(?P<quote>['"])(.*?)(?P=quote))?\s*,?$""",re.IGNORECASE)
def test_re():
    statement='id integer primary key comment "主键" ,'
    res= COLDEF.match(statement)
    print(res.group(5))
    assert  1==1

def test_parse():
    SQL = """
    CREATE TABLE `hello`.`foo_1_0` (
             id integer primary key comment '主键',
             title varchar(200) not null,
             `description` text,
             `salary` FLOAT,
             key(title,description)
             );
    """

    SQL2="""
    CREATE TABLE daily_audit_stat (
id int(11) NOT NULL AUTO_INCREMENT primary key,
logdate date comment '日期',
audit_object varchar(20) comment '审核对象: 帖子，评论，动态',
model_name varchar(100) comment '模型名称:all，模型名字',
model_input_num bigint  comment '模型进审量、机审进审量',
model_pass_num bigint  comment  '模型过审量、机审过审量',
model_delete_num bigint  comment  '模型删除数',
model_recovery_num bigint  comment '机审删除后恢复数量',
final_pass_num bigint  comment '最终通过量',
manul_num bigint comment  '送人审数量',
op_deleted_num bigint comment 'op删除数',
admin_deleted_num bigint comment '版主删除数',
`is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
)
ENGINE=InnoDB AUTO_INCREMENT=1986 DEFAULT CHARSET=utf8 COMMENT='审核统计'
    """


    SQL3="""create table hello.daily_audit_stat(
id int(11) NOT NULL AUTO_INCREMENT primary key,
logdate date comment '日期',
audit_object varchar(20) comment '审核对象: 帖子，评论，动态',
model_name varchar(100) comment '模型名称:all，模型名字',
model_input_num bigint  comment '模型进审量、机审进审量',
model_pass_num bigint  comment  '模型过审量、机审过审量',
model_delete_num bigint  comment  '模型删除数',
model_recovery_num bigint  comment '机审删除后恢复数量',
final_pass_num bigint  comment '最终通过量',
manul_num bigint comment  '送人审数量',
op_deleted_num bigint comment 'op删除数',
admin_deleted_num bigint comment '版主删除数',
`is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间')
ENGINE=InnoDB AUTO_INCREMENT=1986 DEFAULT CHARSET=utf8 COMMENT='审核统计';
"""

    # parser = ColumnsExtract(SQL)
    # parser.parse()
    # print(parser.table_name)
    # print(parser.comments)
    # print(parser.coltypes)
    # print(parser.formatted_columns())
    # print(parser.formatted_columns('"',',\n'))
    # ddl1 = parser.to_hive_ddl()
    # ddl2=parser.to_doris_ddl()
    # print(ddl2)
    parser = ColumnsExtract(SQL3)
    parser.parse()