<template>
  <div class="shell">
    <header class="header">
      <div class="title">智能钻孔车</div>
      <div class="user-panel">
        <div class="avatar" aria-hidden="true"></div>
        <div class="user-info">
          <div class="label">当前用户</div>
          <div class="value">AAAAAA</div>
        </div>
        <div class="clock">{{ clockText }}</div>
      </div>
    </header>

    <main>
      <section class="screens">
        <div
          class="screen"
          :class="{ active: activeScreen === 'screen-main' }"
          v-show="activeScreen === 'screen-main'"
        >
          <div class="main-layout">
            <div class="visual-block card">
              <div class="diagram">
                <div class="machine"></div>
                <ul class="labels">
                  <li v-for="label in diagramLabels" :key="label">{{ label }}</li>
                </ul>
              </div>
              <div class="depth-input">
                <label>打孔深度编号</label>
                <input v-model.number="depthId" type="number" min="0" />
                <button @click="confirmDepth">打孔确认</button>
                <button 
                  @mousedown="handleStartDrillHoleDown"
                  @mouseup="handleStartDrillHoleUp"
                  @mouseleave="handleStartDrillHoleUp"
                  @touchstart="handleStartDrillHoleDown"
                  @touchend="handleStartDrillHoleUp"
                >
                  开始打孔
                </button>
                <div class="depth-display">
                  <div class="depth-item">
                    <label>设定深度</label>
                    <div class="depth-value">{{ setDepth }}</div>
                  </div>
                  <div class="depth-item">
                    <label>当前深度</label>
                    <div class="depth-value">{{ currentDepth }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="manual-block card">
              <div class="joystick-buttons">
                <button
                  v-for="button in joystickButtons"
                  :key="button.id"
                  :class="button.class"
                    @mousedown="handleButtonDown(button.id, button.label)"
                  @mouseup="handleButtonUp(button.id)"
                  @mouseleave="handleButtonUp(button.id)"
                  @touchstart="handleButtonDown(button.id, button.label)"
                  @touchend="handleButtonUp(button.id)"
                >
                  {{ button.label }}
                </button>
              </div>
              <div class="auto-row">
                <label class="toggle">
                  <input type="checkbox" v-model="autoMode" @change="handleAutoMode" />
                  <span>自动模式</span>
                </label>
                <div class="auto-buttons">
                  <button 
                    :class="{ active: startButtonState }"
                    @mousedown="handleStartButtonDown"
                    @mouseup="handleStartButtonUp"
                    @mouseleave="handleStartButtonUp"
                    @touchstart="handleStartButtonDown"
                    @touchend="handleStartButtonUp"
                  >
                    <span class="button-light" :class="{ on: startButtonState }"></span>
                    启动
                  </button>
                  <button 
                    :class="{ active: resetButtonState }"
                    @mousedown="handleResetButtonDown"
                    @mouseup="handleResetButtonUp"
                    @mouseleave="handleResetButtonUp"
                    @touchstart="handleResetButtonDown"
                    @touchend="handleResetButtonUp"
                  >
                    <span class="button-light" :class="{ on: resetButtonState }"></span>
                    复位
                  </button>
                  <button 
                    :class="{ active: stopButtonState }"
                    @click="handleStopButtonClick"
                  >
                    <span class="button-light" :class="{ on: stopButtonState }"></span>
                    停止
                  </button>
                  <button 
                    :class="{ active: !emgButtonLocalState }"
                    @click="handleEmgButtonClick"
                  >
                    <span class="button-light" :class="{ on: !emgButtonLocalState }"></span>
                    急停
                  </button>
                </div>
                <div class="indicator">
                  <div class="indicator-title">消息提示</div>
                  <div id="message" :data-type="messageType">{{ message }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="panel-row">
            <div class="panel block">
              <header>取芯钻</header>
              <div class="controls">
                <button
                  v-for="btn in controlButtons.core"
                  :key="btn.id"
                  @mousedown="handleButtonDown(btn.id, btn.label)"
                  @mouseup="handleButtonUp(btn.id)"
                  @mouseleave="handleButtonUp(btn.id)"
                  @touchstart="handleButtonDown(btn.id, btn.label)"
                  @touchend="handleButtonUp(btn.id)"
                >
                  {{ btn.label }}
                </button>
              </div>
            </div>
            <div class="panel block">
              <header>小臂油缸</header>
              <div class="controls">
                <button
                  v-for="btn in controlButtons.arm"
                  :key="btn.id"
                  @mousedown="handleButtonDown(btn.id, btn.label)"
                  @mouseup="handleButtonUp(btn.id)"
                  @mouseleave="handleButtonUp(btn.id)"
                  @touchstart="handleButtonDown(btn.id, btn.label)"
                  @touchend="handleButtonUp(btn.id)"
                >
                  {{ btn.label }}
                </button>
              </div>
            </div>
            <div class="panel block">
              <header>压紧伺服轴</header>
              <div class="controls">
                <button
                  v-for="btn in controlButtons.press"
                  :key="btn.id"
                  @mousedown="handleButtonDown(btn.id, btn.label)"
                  @mouseup="handleButtonUp(btn.id)"
                  @mouseleave="handleButtonUp(btn.id)"
                  @touchstart="handleButtonDown(btn.id, btn.label)"
                  @touchend="handleButtonUp(btn.id)"
                >
                  {{ btn.label }}
                </button>
              </div>
            </div>
            <div class="panel block">
              <header>进给伺服轴</header>
              <div class="controls">
                <button
                  v-for="btn in controlButtons.feed"
                  :key="btn.id"
                  :class="{ disabled: feedPaused }"
                  @mousedown="handleButtonDown(btn.id, btn.label)"
                  @mouseup="handleButtonUp(btn.id)"
                  @mouseleave="handleButtonUp(btn.id)"
                  @touchstart="handleButtonDown(btn.id, btn.label)"
                  @touchend="handleButtonUp(btn.id)"
                >
                  {{ btn.label }}
                </button>
              </div>
            </div>
          </div>

          <div class="torque-row">
            <div class="torque-card">
              <div class="torque-label">压紧伺服当前力矩(%)</div>
              <div class="torque-value">{{ torque1 }}</div>
            </div>
            <div class="torque-card">
              <div class="torque-label">进给伺服当前力矩(%)</div>
              <div class="torque-value">{{ torque2 }}</div>
            </div>
          </div>

          <div class="init-row">
            <div class="init-status" :class="{ done: initDone }">
              {{ initDone ? "已初始化" : "待初始化" }}
            </div>
            <button 
              class="init-btn" 
              @mousedown="handleInitDown"
              @mouseup="handleInitUp"
              @mouseleave="handleInitUp"
              @touchstart="handleInitDown"
              @touchend="handleInitUp"
            >
              初始化
            </button>
          </div>

          <div class="diagnostics">
            <div class="alarm-list">
              <div v-for="tip in alarmTips" :key="tip">{{ tip }}</div>
            </div>
            <div class="notice">{{ noticeText }}</div>
          </div>

        </div>

        <div
          class="screen"
          :class="{ active: activeScreen === 'screen-rotate' }"
          v-show="activeScreen === 'screen-rotate'"
        >
          <ServoPanel
            title="回转伺服轴"
            :points="servoPoints.rotate"
            :unit="{ pos: '°', speed: '°/s' }"
            positionKey="rotate_data_p_cur"
            speedKey="rotate_data_v_cur"
            jog-positive-key="rotate_right"
            jog-negative-key="rotate_left"
            jog-speed-key="rotate_data_v_jog"
            teach-index-key="rotate_teach_index"
            cur-index-key="rotate_cur_index"
            manual-speed-key="rotate_abs_manual_speed"
            teach-order-key="rotate_order_teach"
            manual-move-key="rotate_order_manual_move"
          />
        </div>

        <div
          class="screen"
          :class="{ active: activeScreen === 'screen-press' }"
          v-show="activeScreen === 'screen-press'"
        >
          <ServoPanel
            title="压紧伺服轴"
            :points="servoPoints.press"
            :unit="{ pos: 'mm', speed: 'mm/s' }"
            positionKey="press_data_p_cur"
            speedKey="press_data_v_cur"
            jog-positive-key="press_up"
            jog-negative-key="press_down"
            jog-speed-key="press_data_v_jog"
            teach-index-key="press_teach_index"
            cur-index-key="press_cur_index"
            manual-speed-key="press_abs_manual_speed"
            teach-order-key="press_order_teach"
            manual-move-key="press_order_manual_move"
          />
        </div>

        <div
          class="screen"
          :class="{ active: activeScreen === 'screen-feed' }"
          v-show="activeScreen === 'screen-feed'"
        >
          <ServoPanel
            title="进给伺服轴"
            :points="servoPoints.feed"
            :unit="{ pos: 'mm', speed: 'mm/s' }"
            feed
            positionKey="feed_data_p_cur"
            speedKey="feed_data_v_cur"
            jog-positive-key="feed_extend"
            jog-negative-key="feed_shrink"
            jog-speed-key="feed_data_v_jog"
            teach-index-key="feed_teach_index"
            cur-index-key="feed_cur_index"
            manual-speed-key="feed_abs_manual_speed"
            teach-order-key="feed_order_teach"
            manual-move-key="feed_order_manual_move"
            origin-define-key="feed_order_origin_define"
          />
        </div>
      </section>
    </main>

    <footer class="footer">
      <button
        v-for="item in navItems"
        :key="item.id"
        class="footer-btn nav-btn"
        :class="{ active: activeScreen === item.target }"
        @click="activeScreen = item.target"
      >
        <span class="icon" :class="item.icon"></span>
        <span>{{ item.label }}</span>
      </button>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import ServoPanel from "./components/ServoPanel.vue";

const navItems = [
  { id: 1, label: "主界面", target: "screen-main", icon: "home" },
  { id: 2, label: "回转伺服设置", target: "screen-rotate", icon: "rotate" },
  { id: 3, label: "压紧伺服设置", target: "screen-press", icon: "press" },
  { id: 4, label: "进给伺服设置", target: "screen-feed", icon: "feed" },
];

const apiBase = import.meta.env.VITE_API_BASE || "";
const diagramLabels = ["取芯钻", "回转伺服", "小臂油缸", "压紧伺服", "进给伺服"];
const joystickButtons = [
  { id: "rotate_left", label: "左转", class: "grid-left" },
  { id: "move_up", label: "上升", class: "grid-up" },
  { id: "rotate_right", label: "右转", class: "grid-right" },
  { id: "move_down", label: "下降", class: "grid-down" },
];
const alarmTips = ref(["手动", "停机", "无故障"]);

const controlButtons = {
  core: [
    { id: "core_drill_start", label: "启动" },
    { id: "core_drill_stop", label: "停止" },
  ],
  arm: [
    { id: "arm_shrink", label: "缩回" },
    { id: "arm_extend", label: "伸出" },
  ],
  press: [
    { id: "press_up", label: "抬起" },
    { id: "press_down", label: "压紧" },
  ],
  feed: [
    { id: "feed_extend", label: "伸出" },
    { id: "feed_shrink", label: "缩回" },
  ],
};

const rotatePointLabels = [
  "0 待机位",
  "1 定位点1",
  "2 定位点2",
  "3 定位点3",
  "4 定位点4",
  "5 定位点5",
  "6 定位点6",
  "7 备用位4",
  "8 备用位5",
  "9 备用位6",
];

const servoPoints = {
  rotate: rotatePointLabels.map((label, idx) => ({
    label,
    positionKey: `rotate_point_set_${idx}`,
    speedKey: `rotate_abs_auto_${idx}`,
  })),
  press: [
    "0 待机位",
    "1 固定位1",
    "2 固定位2",
    "3 固定位3",
    "4 固定位4",
    "5 固定位5",
    "6 固定位6",
    "7 固定位7",
    "8 固定位8",
    "9 固定位9",
  ].map((label, idx) => ({
    label,
    positionKey: `press_point_set_${idx}`,
    speedKey: `press_abs_auto_${idx}`,
  })),
  feed: [
    "0 采集点",
    "1 穿孔位",
    "2 深度1",
    "3 深度2",
    "4 深度3",
    "5 深度4",
    "6 深度5",
    "7 深度6",
    "8 深度7",
    "9 深度8",
  ].map((label, idx) => ({
    label,
    positionKey: `feed_point_set_${idx}`,
    speedKey: `feed_abs_auto_${idx}`,
  })),
};

const activeScreen = ref("screen-main");
const clockText = ref("--");
const depthId = ref(0);
const depthIdLoaded = ref(false);
const autoMode = ref(false);
const message = ref("自动，停机，无故障");
const messageType = ref("info");
const pressPos = ref("0000.000");
const pressSpeed = ref("0000.000");
const torque1 = ref("0.000");
const torque2 = ref("0.000");
const setDepth = ref("0.000");
const currentDepth = ref("0.000");
const feedPaused = ref(false);
const initDone = ref(false);
// 记录每个动作当前开/关状态，用于"按一次启动，再按一次停止"
const actionStates = ref({});
// 按钮状态（用于指示灯显示）
const startButtonState = ref(false);
const resetButtonState = ref(false);
const stopButtonState = ref(false);
const emgButtonState = ref(false);
// 急停按钮的本地切换状态（独立于后端读取的状态）
const emgButtonLocalState = ref(false);

const noticeText = ref("设备正确，暂无异常报警！");
const intervals = [];

const updateClock = () => {
  const now = new Date();
  clockText.value = now.toISOString().replace("T", " ").substring(0, 19);
};

const setMessage = (text, type = "info") => {
  message.value = text;
  messageType.value = type;
};

const sendCommand = async (action, value = true) => {
  if (!action) {
    setMessage("未找到对应的动作标识", "warn");
    return false;
  }

  if (!apiBase) {
    setMessage("未配置后端地址，无法下发指令", "warn");
    return false;
  }

  try {
    const response = await fetch(`${apiBase}/api/registers/write`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, value }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || "指令下发失败");
    }
    setMessage(data.message || "指令已下发");
    return true;
  } catch (error) {
    console.error(error);
    setMessage(error.message || "网络异常，未能下发指令", "warn");
    return false;
  }
};

const confirmDepth = async () => {
  if (!depthId.value || depthId.value <= 0) {
    setMessage("深度编号必须大于0才能启动", "warn");
    autoMode.value = false;
    return;
  }
  const success = await sendCommand("depth_number", Number(depthId.value));
  if (success) {
    setMessage(`已锁定深度编号 ${depthId.value}`, "info");
  }
};

// 开始打孔按钮：点动模式（按下True，松开False）
const handleStartDrillHoleDown = async () => {
  await sendCommand("start_drill_hole", true);
};

const handleStartDrillHoleUp = async () => {
  await sendCommand("start_drill_hole", false);
};

const handleAutoMode = async () => {
  // 前端UI：勾选表示自动，未勾选表示手动
  // 后端逻辑：true=手动，false=自动，需要取反发送
  const targetAuto = autoMode.value;
  if (targetAuto && (!depthId.value || depthId.value <= 0)) {
    setMessage("请先设定深度编号", "warn");
    autoMode.value = false; // 回退为手动
    return;
  }
  // 前端true=自动，后端true=手动，所以发送时取反
  const success = await sendCommand("auto_mode", !targetAuto);
  if (!success) {
    autoMode.value = !autoMode.value; // 发送失败回滚勾选
    return;
  }
  setMessage(targetAuto ? "自动模式已准备，等待启动" : "已退出自动模式");
};

// 启动按钮：按下为True，松开为False
const handleStartButtonDown = async () => {
  await sendCommand("start_button", true);
};

const handleStartButtonUp = async () => {
  await sendCommand("start_button", false);
};

// 复位按钮：按下为True，松开为False
const handleResetButtonDown = async () => {
  await sendCommand("reset_button", true);
};

const handleResetButtonUp = async () => {
  await sendCommand("reset_button", false);
};

// 停止按钮：切换模式（按下一次True，再按下一次False）
const handleStopButtonClick = async () => {
  const next = !stopButtonState.value;
  await sendCommand("stop_button", next);
};

// 急停按钮：切换模式（按一下True，再按一下False）
// 使用独立的本地状态，不依赖后端读取的状态
// 逻辑：前端亮灯（emgButtonLocalState=false）时发送False，前端灭灯（emgButtonLocalState=true）时发送True
const handleEmgButtonClick = async () => {
  // 切换本地状态
  emgButtonLocalState.value = !emgButtonLocalState.value;
  // 向后端发送值：false（亮灯）或 true（灭灯）
  await sendCommand("emg_button", emgButtonLocalState.value);
};
// 按下按钮时发送True信号
const handleButtonDown = async (actionId, label) => {
  if (!actionId) return;
  // 如果按钮被禁用（如进给伺服暂停时），不执行
  if (actionId.startsWith("feed_") && feedPaused.value) return;
  
  actionStates.value[actionId] = true;
  setMessage(`执行动作：${label} (启动)`, "info");
  await sendCommand(actionId, true);
};

// 松开按钮时发送False信号
const handleButtonUp = async (actionId) => {
  if (!actionId) return;
  // 如果按钮被禁用（如进给伺服暂停时），不执行
  if (actionId.startsWith("feed_") && feedPaused.value) return;
  
  // 只有在按下状态时才发送False
  if (actionStates.value[actionId]) {
    actionStates.value[actionId] = false;
    await sendCommand(actionId, false);
  }
};

// 初始化按钮：点动模式（按下True，松开False）
const handleInitDown = async () => {
  await sendCommand("init_button", true);
};

const handleInitUp = async () => {
  await sendCommand("init_button", false);
};

const updatePressState = () => {
  const target = autoMode.value ? 120 : 30;
  const current = parseFloat(pressPos.value);
  const next = current + (target - current) * 0.1;
  pressPos.value = next.toFixed(3);
  pressSpeed.value = (Math.random() * 20).toFixed(3);
};

const pauseFeed = () => {
  if (feedPaused.value) return;
  feedPaused.value = true;
  setTimeout(() => {
    feedPaused.value = false;
    setMessage("力矩恢复，继续进给", "info");
  }, 1500);
};

const updateTorque = async () => {
  if (!apiBase) {
    torque1.value = "0.000";
    torque2.value = "0.000";
    return;
  }
  try {
    const response = await fetch(`${apiBase}/api/registers/read`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        actions: ["press_data_t_cur", "feed_data_t_cur"], // 压紧伺服当前力矩 和 进给伺服当前力矩
      }),
    });
    if (!response.ok) {
      return;
    }
    const data = await response.json();
    const values = data.values || {};
    const t1 = Number(values.press_data_t_cur ?? 0); // 压紧伺服当前力矩
    const t2 = Number(values.feed_data_t_cur ?? 0);  // 进给伺服当前力矩
    torque1.value = t1.toFixed(3);
    torque2.value = t2.toFixed(3);
  } catch (e) {
    console.error("读取力矩失败", e);
  }
};

// 读取模式 / 初始化 / 故障状态，刷新顶部三段提示
// 注意：此函数仅读取寄存器值用于显示，不会修改任何后端寄存器的值
// 这些寄存器由PLC控制，前端只读不写
const updateAlarmStatus = async () => {
  if (!apiBase) return;
  // 以下寄存器均为只读，仅用于显示状态，不会写入
  const actions = [
    "auto_mode",        // 模式状态（只读显示）
    "home_done_flag",   // 回零完成标志（兼容旧版本）
    "init_status_register",   // 初始化状态寄存器（M56）
    "start_button",     // 启动按钮状态（只读显示）
    "reset_button",     // 复位按钮状态（只读显示）
    "stop_button",      // 停止按钮状态（只读显示）
    "emg_button",       // 急停按钮状态（只读显示）
    "depth_number",     // 打孔深度编号（只读显示）
    // 伺服自身报警（只读）
    "rotate_status_err",
    "press_status_err",
    "feed_status_err",
    // PLC 报警位（只读）
    "alarm_base_rotate_r_fault",
    "alarm_base_rotate_r_pos_limit",
    "alarm_base_rotate_r_neg_limit",
    "alarm_base_rotate_r_not_enabled",
    "alarm_base_rotate_r_not_homed",
    "alarm_base_rotate_r_offline",
    "alarm_fix_axis_fault",
    "alarm_fix_axis_pos_limit",
    "alarm_fix_axis_neg_limit",
    "alarm_fix_axis_not_enabled",
    "alarm_fix_axis_not_homed",
    "alarm_fix_axis_offline",
    "alarm_ctrl_axis_fault",
    "alarm_ctrl_axis_pos_limit",
    "alarm_ctrl_axis_neg_limit",
    "alarm_ctrl_axis_not_enabled",
    "alarm_ctrl_axis_not_homed",
    "alarm_ctrl_axis_offline",
    "alarm_support_not_extended",
    "alarm_depth_code_not_set",
    "alarm_emg_stop",
    "alarm_lift_cyl_fault",
    "alarm_angle_cyl_fault",
  ];
  try {
    // 仅读取，不写入
    const response = await fetch(`${apiBase}/api/registers/read`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ actions }),
    });
    if (!response.ok) return;
    const data = await response.json();
    const values = data.values || {};
    // 后端逻辑：true=手动，false=自动；前端UI：true=自动，false=手动，需要取反
    const isAuto = !values.auto_mode;
    // 仅更新前端显示状态，不会触发写入操作（程序设置不会触发@change事件）
    autoMode.value = isAuto;
    // 更新初始化状态 - 使用M56寄存器（init_status_register）
    const isInited = !!values.init_status_register;
    initDone.value = isInited;
    // 更新按钮状态（用于指示灯显示）
    startButtonState.value = !!values.start_button;
    resetButtonState.value = !!values.reset_button;
    stopButtonState.value = !!values.stop_button;
    emgButtonState.value = !!values.emg_button;
    // 更新深度编号（只读显示）- 只在第一次加载时读取
    if (values.depth_number !== undefined && !depthIdLoaded.value) {
      depthId.value = Number(values.depth_number);
      depthIdLoaded.value = true;
    }
    // 只要以上任何报警位为 true，则认为"有故障"
    const hasFault = Object.entries(values).some(([key, val]) =>
      !["auto_mode", "home_done_flag", "depth_number"].includes(key) ? !!val : false
    );

    // 仅用于显示，不修改后端寄存器
    const modeText = isAuto ? "自动" : "手动";
    const stopText = isInited ? "运行" : "停机";
    const faultText = hasFault ? "有故障" : "无故障";

    alarmTips.value = [modeText, stopText, faultText];
    noticeText.value = hasFault
      ? "设备存在故障，请检查报警！"
      : "设备正确，暂无异常报警！";
  } catch (error) {
    console.error("读取报警状态失败", error);
  }
};

// 读取设定深度和当前深度寄存器值
const updateDepthValues = async () => {
  if (!apiBase) {
    setDepth.value = "0.000";
    currentDepth.value = "0.000";
    return;
  }
  try {
    const response = await fetch(`${apiBase}/api/registers/read`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        actions: ["set_depth", "current_depth"], // 设定深度 和 当前深度
      }),
    });
    if (!response.ok) {
      return;
    }
    const data = await response.json();
    const values = data.values || {};
    const sDepth = Number(values.set_depth ?? 0); // 设定深度
    const cDepth = Number(values.current_depth ?? 0);  // 当前深度
    setDepth.value = sDepth.toFixed(3);
    currentDepth.value = cDepth.toFixed(3);
  } catch (e) {
    console.error("读取深度值失败", e);
  }
};


onMounted(() => {
  updateClock();
  intervals.push(setInterval(updateClock, 1000));
  intervals.push(setInterval(updatePressState, 500));
  updateTorque(); // 立即执行一次
  intervals.push(setInterval(updateTorque, 500)); // 每500ms刷新一次转矩值
  updateAlarmStatus(); // 立即执行一次
  intervals.push(setInterval(updateAlarmStatus, 1000)); // 每1秒刷新一次模式/初始化/故障状态/按钮状态
  updateDepthValues(); // 立即执行一次深度值读取
  intervals.push(setInterval(updateDepthValues, 500)); // 每500ms刷新一次深度值
  // 急停按钮信号每5秒保持一次，使用当前本地状态
  intervals.push(setInterval(() => sendCommand("emg_button", emgButtonLocalState.value), 5000));
});

onBeforeUnmount(() => {
  intervals.forEach(clearInterval);
});
</script>

<style scoped>
.depth-display {
  display: flex;
  gap: 15px;
  margin-left: 15px;
  align-items: center;
}

.depth-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.depth-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.depth-value {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  background-color: #f5f5f5;
  padding: 6px 12px;
  border-radius: 4px;
  min-width: 80px;
  text-align: center;
}
</style>

