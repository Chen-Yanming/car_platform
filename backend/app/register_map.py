REGISTER_MAP = {
  # 摇杆四向
  # 角度油缸缩回 / 伸出
  "angle_cyl_shrink": {
    "name": "角度油缸缩回",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 12",
    "group_id": 2,
  },
  "angle_cyl_extend": {
    "name": "角度油缸伸出",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 13",
    "group_id": 2,
  },
  # 右旋转 / 左旋转（用于回转伺服 JOG+/JOG-）
  "rotate_right": {
    "name": "右旋转",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 18",
    "group_id": 2,
  },
  "rotate_left": {
    "name": "左旋转",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 19",
    "group_id": 2,
  },
  "move_up": {
    "name": "钻机抬升",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 11",
    "group_id": 2,
  },
  "move_down": {
    "name": "钻机下降",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 10",
    "group_id": 2,
  },
  # 取芯钻
  "core_drill_start": {
    "name": "钻机启动",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 20",
    "group_id": 2,
  },
  "core_drill_stop": {
    "name": "钻机停止",
    "connection": "Smart car",
    "data_type": "Bool",
    # 表格中没有单独的“停止”位，这里与启动共用同一地址，区别在于写入 true/false
    "address": "1 M 20",
    "group_id": 2,
  },
  # 小臂油缸
  "arm_shrink": {
    "name": "油缸下降",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 12",
    "group_id": 2,
  },
  "arm_extend": {
    "name": "油缸上升",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 13",
    "group_id": 2,
  },
  # 压紧伺服轴
  "press_up": {
    "name": "钻机抬升",
    "connection": "Smart car",
    "data_type": "Bool",
    # 钻机固定松开
    "address": "1 M 15",
    "group_id": 2,
  },
  "press_down": {
    "name": "钻机下降",
    "connection": "Smart car",
    "data_type": "Bool",
    # 钻机固定下压
    "address": "1 M 14",
    "group_id": 2,
  },
  # 进给伺服轴
  "feed_extend": {
    "name": "取芯钻伸出",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 16",
    "group_id": 2,
  },
  "feed_shrink": {
    "name": "取芯钻缩回",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 17",
    "group_id": 2,
  },
  # 模式与深度
  # 注意：auto_mode 寄存器逻辑：true=手动模式，false=自动模式
  # 前端UI已做取反处理，前端true=自动，false=手动
  "auto_mode": {
    "name": "自动打孔转换按钮",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 40",
    "group_id": 2,
  },
  "depth_number": {
    "name": "深度选择",
    "connection": "Smart car",
    "data_type": "Int16",
    # 表格：深度选择 Int16 长度2  地址 1 D 100
    "address": "1 D 100",
    "group_id": 2,
  },
  "depth_display": {
    "name": "深度显示",
    "connection": "Smart car",
    "data_type": "Int32",
    # 表格：深度显示 Int32 长度4 地址 1 D 102
    "address": "1 D 102",
    "group_id": 2,
  },
  "init_button": {
    "name": "初始化按钮",
    "connection": "Smart car",
    "data_type": "Bool",
    # 与“回零完成标志”共用 M33
    "address": "1 M 33",
    "group_id": 2,
  },
  "drill_home": {
    "name": "钻机回原点",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 30",
    "group_id": 2,
  },
  "home_done_flag": {
    "name": "回零完成标志",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 33",
    "group_id": 2,
  },
  # 启动 / 复位 / 停止 / 急停 物理按钮映射的虚拟按键
  "start_button": {
    "name": "启动按钮",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 50",
    "group_id": 2,
  },
  "reset_button": {
    "name": "复位按钮",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 51",
    "group_id": 2,
  },
  "stop_button": {
    "name": "停止按钮",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 52",
    "group_id": 2,
  },
  "emg_button": {
    "name": "急停按钮(常闭)",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 53",
    "group_id": 2,
  },
  "manual_position_button": {
    "name": "打孔手动定位按钮",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 34",
    "group_id": 2,
  },
  "start_drill_hole": {
    "name": "开始打孔",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 27",
    "group_id": 2,
  },
  "buzzer_mute": {
    "name": "蜂鸣器屏蔽",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 36",
    "group_id": 2,
  },
  # 故障与报警信号（aAL0[...] -> M110 ~）
  "alarm_base_rotate_r_fault": {
    "name": "底座旋转R轴故障",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 110",
    "group_id": 2,
  },
  "alarm_base_rotate_r_pos_limit": {
    "name": "底座旋转R轴正极限报警",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 111",
    "group_id": 2,
  },
  "alarm_base_rotate_r_neg_limit": {
    "name": "底座旋转R轴负极限报警",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 112",
    "group_id": 2,
  },
  "alarm_base_rotate_r_not_enabled": {
    "name": "底座旋转R轴未使能",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 113",
    "group_id": 2,
  },
  "alarm_base_rotate_r_not_homed": {
    "name": "底座旋转R轴未回原点",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 114",
    "group_id": 2,
  },
  "alarm_base_rotate_r_offline": {
    "name": "底座旋转R轴掉线",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 115",
    "group_id": 2,
  },
  "alarm_fix_axis_fault": {
    "name": "电钻固定轴故障",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 116",
    "group_id": 2,
  },
  "alarm_fix_axis_pos_limit": {
    "name": "电钻固定轴正极限报警",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 117",
    "group_id": 2,
  },
  "alarm_fix_axis_neg_limit": {
    "name": "电钻固定轴负极限报警",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 118",
    "group_id": 2,
  },
  "alarm_fix_axis_not_enabled": {
    "name": "电钻固定轴未使能",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 119",
    "group_id": 2,
  },
  "alarm_fix_axis_not_homed": {
    "name": "电钻固定轴未回原点",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 120",
    "group_id": 2,
  },
  "alarm_fix_axis_offline": {
    "name": "电钻固定轴掉线",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 121",
    "group_id": 2,
  },
  "alarm_ctrl_axis_fault": {
    "name": "打孔控制轴故障",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 122",
    "group_id": 2,
  },
  "alarm_ctrl_axis_pos_limit": {
    "name": "打孔控制轴正极限报警",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 123",
    "group_id": 2,
  },
  "alarm_ctrl_axis_neg_limit": {
    "name": "打孔控制轴负极限报警",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 124",
    "group_id": 2,
  },
  "alarm_ctrl_axis_not_enabled": {
    "name": "打孔控制轴未使能",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 125",
    "group_id": 2,
  },
  "alarm_ctrl_axis_not_homed": {
    "name": "打孔控制轴未回原点",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 126",
    "group_id": 2,
  },
  "alarm_ctrl_axis_offline": {
    "name": "打孔控制轴掉线",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 127",
    "group_id": 2,
  },
  "alarm_support_not_extended": {
    "name": "钻机固定支架未伸出报警",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 128",
    "group_id": 2,
  },
  "alarm_depth_code_not_set": {
    "name": "打孔深度编码号未设置",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 129",
    "group_id": 2,
  },
  "init_status_register": {
    "name": "初始化状态寄存器",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "M 56",
    "group_id": 2,
  },
  "alarm_emg_stop": {
    "name": "紧急停止",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 140",
    "group_id": 2,
  },
  "alarm_lift_cyl_fault": {
    "name": "举升油缸故障",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 141",
    "group_id": 2,
  },
  "alarm_angle_cyl_fault": {
    "name": "角度油缸故障",
    "connection": "Smart car",
    "data_type": "Bool",
    "address": "1 M 142",
    "group_id": 2,
  },
  # 回转伺服轴控制与参数
  "rotate_order_enable": {
    "name": "回转伺服使能",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1895.2",
  },
  "rotate_order_manual_home": {
    "name": "回转伺服手动回原点",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1895.3",
  },
  "rotate_order_jog_up": {
    "name": "回转伺服正向点动",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1895.5",
  },
  "rotate_order_jog_down": {
    "name": "回转伺服反向点动",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1895.6",
  },
  "rotate_order_disable": {
    "name": "回转伺服强制断使能",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1895.10",
  },
  "rotate_order_manual_move": {
    "name": "回转伺服手动绝对定位按钮",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1895.15",
  },
  "rotate_order_teach": {
    "name": "回转伺服示教",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1896.0",
  },
  "rotate_status_enabled": {
    "name": "回转伺服使能状态",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1897.1",
  },
  "rotate_status_err": {
    "name": "回转伺服报警状态",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1897.8",
  },
  "rotate_status_homed": {
    "name": "回转伺服自动回原标志",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1897.9",
  },
  "rotate_data_p_cur": {
    "name": "回转当前位置",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1900",
  },
  "rotate_data_v_cur": {
    "name": "回转当前速度",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1902",
  },
  "rotate_data_t_cur": {
    "name": "回转当前转矩",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1904",
  },
  "rotate_data_v_jog": {
    "name": "回转点动速度",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1906",
  },
  # 压紧伺服轴控制与参数（按压紧伺服轴表）
  "press_order_enable": {
    "name": "压紧伺服使能",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1400.2",
  },
  "press_order_manual_home": {
    "name": "压紧伺服手动回原点",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1400.3",
  },
  "press_order_jog_up": {
    "name": "压紧伺服正向点动",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1400.5",
  },
  "press_order_jog_down": {
    "name": "压紧伺服反向点动",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1400.6",
  },
  "press_order_disable": {
    "name": "压紧伺服强制断使能",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1400.10",
  },
  "press_order_manual_move": {
    "name": "压紧伺服手动绝对定位按钮",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1400.15",
  },
  "press_order_teach": {
    "name": "压紧伺服示教",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1401.0",
  },
  "press_status_enabled": {
    "name": "压紧伺服使能状态",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1402.1",
  },
  "press_status_err": {
    "name": "压紧伺服报警状态",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1402.8",
  },
  "press_status_clamp_ok": {
    "name": "电钻固定位到位",
    "connection": "axis",
    "data_type": "Bool",
    "address": "D1402.9",
  },
  "press_data_p_cur": {
    "name": "压紧当前位置",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1405",
  },
  "press_data_v_cur": {
    "name": "压紧当前速度",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1407",
  },
  "press_data_t_cur": {
    "name": "压紧伺服当前力矩",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1409",  # 压紧伺服当前力矩
  },
  "press_data_v_jog": {
    "name": "压紧点动速度",
    "connection": "axis",
    "data_type": "Real",
    "address": "D1411",
  },
}

# 回转伺服点位与参数
for index, addr in enumerate(
  [1930, 1933, 1935, 1937, 1939, 1941, 1943, 1945, 1947, 1949]
):
  REGISTER_MAP[f"rotate_point_set_{index}"] = {
    "name": f"回转待机点位{index}",
    "connection": "axis",
    "data_type": "Real",
    "address": f"D{addr}",
  }

for index, addr in enumerate(
  [1973, 1975, 1977, 1979, 1981, 1983, 1985, 1987, 1989, 1991]
):
  REGISTER_MAP[f"rotate_abs_auto_{index}"] = {
    "name": f"回转自动速度{index}",
    "connection": "axis",
    "data_type": "Real",
    "address": f"D{addr}",
  }

REGISTER_MAP["rotate_abs_manual_speed"] = {
  "name": "回转手动速度",
  "connection": "axis",
  "data_type": "Real",
  "address": "D2011",
}

REGISTER_MAP["rotate_teach_index"] = {
  "name": "回转示教步号",
  "connection": "axis",
  "data_type": "Int",
  "address": "D2013",
}

REGISTER_MAP["rotate_cur_index"] = {
  "name": "回转当前位置步号",
  "connection": "axis",
  "data_type": "Int",
  "address": "D2014",
}

# 压紧伺服点位与参数（按表：待机位 + 固定位1~9）
for index, addr in enumerate(
  [1436, 1438, 1440, 1442, 1444, 1446, 1448, 1450, 1452, 1454]
):
  REGISTER_MAP[f"press_point_set_{index}"] = {
    "name": f"压紧固定点位{index}",
    "connection": "axis",
    "data_type": "Real",
    "address": f"D{addr}",
  }

for index, addr in enumerate(
  [1476, 1478, 1480, 1482, 1484, 1486, 1488, 1490, 1492, 1494]
):
  REGISTER_MAP[f"press_abs_auto_{index}"] = {
    "name": f"压紧自动速度{index}",
    "connection": "axis",
    "data_type": "Real",
    "address": f"D{addr}",
  }

REGISTER_MAP["press_abs_manual_speed"] = {
  "name": "压紧手动速度",
  "connection": "axis",
  "data_type": "Real",
  "address": "D1516",
}

REGISTER_MAP["press_teach_index"] = {
  "name": "压紧示教步号",
  "connection": "axis",
  "data_type": "Int",
  "address": "D1518",
}

REGISTER_MAP["press_cur_index"] = {
  "name": "压紧当前位置步号",
  "connection": "axis",
  "data_type": "Int",
  "address": "D1519",
}

# 修改设定深度寄存器地址为D102，当前深度为D104
REGISTER_MAP["set_depth"] = {
  "name": "设定深度",
  "connection": "axis",
  "data_type": "Real",
  "address": "D102",  # 根据需求改为D102
}

REGISTER_MAP["current_depth"] = {
  "name": "当前深度",
  "connection": "axis",
  "data_type": "Real",
  "address": "D104",  # 当前深度使用D104
}

# 进给伺服轴控制与参数（按进给伺服轴表）
REGISTER_MAP.update(
  {
    "feed_order_manual_home": {
      "name": "进给伺服手动回原点",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1565.3",
    },
    "feed_order_jog_up": {
      "name": "进给伺服正向点动",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1565.5",
    },
    "feed_order_jog_down": {
      "name": "进给伺服反向点动",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1565.6",
    },
    "feed_order_disable": {
      "name": "进给伺服强制断使能",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1565.10",
    },
    "feed_order_manual_move": {
      "name": "进给伺服手动绝对定位按钮",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1565.15",
    },
    "feed_order_origin_define": {
      "name": "进给伺服原点定义",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1565.3",
    },
    "feed_order_teach": {
      "name": "进给伺服示教",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1566.0",
    },
    "feed_status_enabled": {
      "name": "进给伺服使能状态",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1567.1",
    },
    "feed_status_err": {
      "name": "进给伺服报警状态",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1567.8",
    },
    "feed_status_ctrl_axis": {
      "name": "打孔控制轴选择",
      "connection": "axis",
      "data_type": "Bool",
      "address": "D1567.9",
    },
    "feed_data_p_cur": {
      "name": "进给当前位置",
      "connection": "axis",
      "data_type": "Real",
      "address": "D1570",
    },
    "feed_data_v_cur": {
      "name": "进给当前速度",
      "connection": "axis",
      "data_type": "Real",
      "address": "D1572",
    },
    "feed_data_v_jog": {
      "name": "进给点动速度",
      "connection": "axis",
      "data_type": "Real",
      "address": "D1576",
    },
    "feed_data_t_cur": {
      "name": "进给伺服当前力矩",
      "connection": "axis",
      "data_type": "Real",
      "address": "D1574",
    },
  }
)

# 进给伺服点位与参数（自动点位 / 自动速度）
for index, addr in enumerate(
  [1601, 1603, 1605, 1607, 1609, 1611, 1613, 1615, 1617, 1619]
):
  REGISTER_MAP[f"feed_point_set_{index}"] = {
    "name": f"进给点位{index}",
    "connection": "axis",
    "data_type": "Real",
    "address": f"D{addr}",
  }

for index, addr in enumerate(
  [1641, 1643, 1645, 1647, 1649, 1651, 1653, 1655, 1657, 1659]
):
  REGISTER_MAP[f"feed_abs_auto_{index}"] = {
    "name": f"进给自动速度{index}",
    "connection": "axis",
    "data_type": "Real",
    "address": f"D{addr}",
  }

REGISTER_MAP["feed_abs_manual_speed"] = {
  "name": "进给手动速度",
  "connection": "axis",
  "data_type": "Real",
  "address": "D1681",
}

REGISTER_MAP["feed_teach_index"] = {
  "name": "进给示教步号",
  "connection": "axis",
  "data_type": "Int",
  "address": "D1683",
}

REGISTER_MAP["feed_cur_index"] = {
  "name": "进给当前位置步号",
  "connection": "axis",
  "data_type": "Int",
  "address": "D1684",
}
