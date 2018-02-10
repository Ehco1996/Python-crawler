### 第三方支付平台 码支付账单 csv爬取

网站地址：https://codepay.fateqq.com/



### 使用步骤

**安装前置依赖**

* `brew/yum/apt-get install python3` # 选择你喜欢的方式安装Python3
* `pip install -r requirements.txt` # 安装第三方库


**配置个人信息**

* 打开`config.py`并配置好自己的mysql数据库信息，码支付的账号和密码
* 保证数据库里有一张名为`91pay`的表

创建的sql语句如下：

```sql
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cmf_pay_orders
-- ----------------------------
DROP TABLE IF EXISTS `cmf_pay_orders`;
CREATE TABLE `cmf_pay_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `username` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '用户名',
  `way` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '支付方式',
  `status` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '订单状态',
  `trade_no` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '订单号',
  `raw_price` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '申请价格',
  `pay_price` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '支付价格',
  `date` datetime DEFAULT NULL COMMENT '订单日期',
  `cash` int(2) NOT NULL DEFAULT '0' COMMENT '提现状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
```


**运行程序**

`python3 spider.py`

ok，今天的账单信息已经入库了