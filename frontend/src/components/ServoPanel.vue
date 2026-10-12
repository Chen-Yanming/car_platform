<template>
  <div class="servo-screen">
    <div class="servo-header">
      <div class="title">{{ title }}</div>
      <div class="switches">
        <label><input type="checkbox" checked /> Enabled</label>
        <label><input type="checkbox" checked /> Home</label>
        <label><input type="checkbox" /> Alarm</label>
      </div>
    </div>
    <div class="servo-body">
      <div class="info-column">
        <div class="value-block">
          <label>当前位置({{ unit.pos }})</label>
          <input :value="positionValue" readonly />
        </div>
        <div class="value-block">
          <label>当前速度({{ unit.speed }})</label>
          <input :value="speedValue" readonly />
        </div>
        <div class="jog-buttons">
          <button
            v-for="btn in manualButtons"
            :key="btn.label"
            @mousedown="handleManualButtonDown(btn)"
            @mouseup="handleManualButtonUp(btn)"
            @mouseleave="handleManualButtonUp(btn)"
            @touchstart="handleManualButtonDown(btn)"
            @touchend="handleManualButtonUp(btn)"
          >
            {{ btn.label }}
          </button>
          <button class="accent" disabled>Home</button>
          <button class="danger" disabled>Disable</button>
        </div>
        <div class="value-block">
          <label>JOG速度</label>
          <input v-model="jogSpeed" @blur="handleJogSpeedBlur" />
        </div>
      </div>
      <div class="position-column">
        <div class="teach-row">
          <label>示教定位号</label>
          <input
            v-model="teachIndex"
          />
          <button @click="handleTeachClick">示教</button>
        </div>
        <div class="teach-row">
          <label>手动定位号</label>
          <input
            v-model="manualIndex"
          />
          <label>手动定位速度</label>
          <input v-model="manualSpeed" />
          <button class="accent" @click="handleManualMoveClick">定位</button>
        </div>
        <div class="point-table">
          <div class="item" v-for="(point, idx) in normalizedPoints" :key="point.label">
            <span>{{ point.label }}</span>
            <input
              v-model="pointValues[idx].position"
              @blur="handlePointBlur(idx, 'position')"
            />
            <input v-model="pointValues[idx].speed" @blur="handlePointBlur(idx, 'speed')" />
          </div>
        </div>
        <div v-if="feed" class="origin-define">
          <button class="accent" @click="handleOriginDefineClick">原点定义</button>
          <span>需回到标记位执行</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from "vue";

const props = defineProps({
  title: String,
  points: {
    type: Array,
    default: () => [],
  },
  unit: Object,
  feed: Boolean,
  // 可选：读取轴的当前位置和速度用的 action 名
  positionKey: String,
  speedKey: String,
  jogPositiveKey: String,
  jogNegativeKey: String,
  // 下面这些主要用于回转伺服轴，其它轴可以不传
  jogSpeedKey: String,
  teachIndexKey: String,
  curIndexKey: String,
  manualSpeedKey: String,
  teachOrderKey: String,
  manualMoveKey: String,
  originDefineKey: String,
});

const apiBase = import.meta.env.VITE_API_BASE || "";

const normalizedPoints = computed(() =>
  props.points.map((pt, idx) =>
    typeof pt === "string"
      ? { label: pt, index: idx }
      : { label: pt.label || `点位${idx}`, index: idx, ...pt }
  )
);

const manualButtons = computed(() => {
  if (props.feed) {
    return [
      { label: "JOG+", action: props.jogPositiveKey },
      { label: "JOG-", action: props.jogNegativeKey },
    ];
  }
  return [
    { label: "JOG+", action: props.jogPositiveKey },
    { label: "JOG-", action: props.jogNegativeKey },
  ];
});

const positionValue = ref("0000.000");
const speedValue = ref("0000.000");
const jogStates = ref({});
const jogSpeed = ref("0000.000");
const teachIndex = ref("00");
const manualIndex = ref("00");
const manualSpeed = ref("0000.000");

const pointValues = ref(
  normalizedPoints.value.map(() => ({ position: "0000.000", speed: "0000.000" }))
);

watch(
  normalizedPoints,
  (val) => {
    pointValues.value = val.map(() => ({ position: "0000.000", speed: "0000.000" }));
    fetchPointValues();
  },
  { immediate: false }
);

const hasPointKeys = computed(() =>
  normalizedPoints.value.some((pt) => pt.positionKey || pt.speedKey)
);

const formatNumber = (value) => {
  if (value === undefined || value === null || Number.isNaN(Number(value))) {
    return "0000.000";
  }
  return Number(value).toFixed(3);
};

const fetchPointValues = async () => {
  if (!apiBase || !hasPointKeys.value) return;
  const actions = [];
  normalizedPoints.value.forEach((pt) => {
    if (pt.positionKey) actions.push(pt.positionKey);
    if (pt.speedKey) actions.push(pt.speedKey);
  });
  if (!actions.length) return;
  try {
    const response = await fetch(`${apiBase}/api/registers/read`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ actions }),
    });
    if (!response.ok) return;
    const data = await response.json();
    const values = data.values || {};
    pointValues.value = pointValues.value.map((pv, idx) => {
      const point = normalizedPoints.value[idx];
      return {
        position: point.positionKey
          ? formatNumber(values[point.positionKey])
          : pv.position,
        speed: point.speedKey ? formatNumber(values[point.speedKey]) : pv.speed,
      };
    });
  } catch (error) {
    console.error("读取点位失败", error);
  }
};

const writeRegister = async (action, value) => {
  if (!apiBase || !action) return;
  try {
    await fetch(`${apiBase}/api/registers/write`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, value }),
    });
  } catch (error) {
    // 静默处理错误，不输出日志
  }
};

const handlePointBlur = async (index, type) => {
  const point = normalizedPoints.value[index];
  const value =
    type === "position"
      ? Number(pointValues.value[index].position)
      : Number(pointValues.value[index].speed);
  const action = type === "position" ? point.positionKey : point.speedKey;
  if (!action || Number.isNaN(value)) return;
  await writeRegister(action, value);
};

// 点动模式：按下为True，松开为False
const handleManualButtonDown = async (btn) => {
  if (!btn.action) return;
  jogStates.value[btn.action] = true;
  await writeRegister(btn.action, true);
};

const handleManualButtonUp = async (btn) => {
  if (!btn.action) return;
  // 只有在按下状态时才发送False
  if (jogStates.value[btn.action]) {
    jogStates.value[btn.action] = false;
    await writeRegister(btn.action, false);
  }
};

const handleJogSpeedBlur = async () => {
  if (!props.jogSpeedKey) return;
  const value = Number(jogSpeed.value);
  if (Number.isNaN(value)) return;
  await writeRegister(props.jogSpeedKey, value);
};


// 示教定位号保存逻辑（只在点击示教按钮时调用）
const handleTeachIndexSave = async () => {
  if (!props.teachIndexKey) return;
  const value = Number(teachIndex.value);
  if (Number.isNaN(value)) return;
  await writeRegister(props.teachIndexKey, value);
};

// 手动定位号和手动定位速度保存逻辑（只在点击定位按钮时调用）
const handleManualValuesSave = async () => {
  if (props.curIndexKey) {
    const indexValue = Number(manualIndex.value);
    if (!Number.isNaN(indexValue)) {
      await writeRegister(props.curIndexKey, indexValue);
    }
  }
  if (props.manualSpeedKey) {
    const speedValue = Number(manualSpeed.value);
    if (!Number.isNaN(speedValue)) {
      await writeRegister(props.manualSpeedKey, speedValue);
    }
  }
};

const handleTeachClick = async () => {
  // 先保存示教定位号
  await handleTeachIndexSave();
  // 然后执行示教命令：先设为True，0.5秒后改回False
  if (props.teachOrderKey) {
    await writeRegister(props.teachOrderKey, true);
    setTimeout(async () => {
      await writeRegister(props.teachOrderKey, false);
    }, 500);
  }
  // 写入后读取示教定位号的值
  if (props.teachIndexKey) {
    await fetchInitialIndexValues();
  }
};

const handleManualMoveClick = async () => {
  // 先保存手动定位号和手动定位速度
  await handleManualValuesSave();
  // 然后执行定位命令：先设为True，0.5秒后改回False
  if (props.manualMoveKey) {
    await writeRegister(props.manualMoveKey, true);
    setTimeout(async () => {
      await writeRegister(props.manualMoveKey, false);
    }, 500);
  }
  // 写入后读取手动定位号和手动定位速度的值
  if (props.curIndexKey || props.manualSpeedKey) {
    await fetchInitialIndexValues();
  }
};

const handleOriginDefineClick = async () => {
  // 执行原点定义命令
  if (props.originDefineKey) {
    await writeRegister(props.originDefineKey, true);
  }
};

// 读取示教定位号和手动定位号的初始值（只在组件挂载时调用）
const fetchInitialIndexValues = async () => {
  if (!apiBase) return;
  const actions = [];
  if (props.teachIndexKey) actions.push(props.teachIndexKey);
  if (props.curIndexKey) actions.push(props.curIndexKey);
  if (props.manualSpeedKey) actions.push(props.manualSpeedKey);
  if (!actions.length) return;
  try {
    const response = await fetch(`${apiBase}/api/registers/read`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ actions }),
    });
    if (!response.ok) return;
    const data = await response.json();
    const values = data.values || {};
    if (props.teachIndexKey && values[props.teachIndexKey] !== undefined) {
      teachIndex.value = String(values[props.teachIndexKey]).padStart(2, "0");
    }
    if (props.curIndexKey && values[props.curIndexKey] !== undefined) {
      manualIndex.value = String(values[props.curIndexKey]).padStart(2, "0");
    }
    if (props.manualSpeedKey && values[props.manualSpeedKey] !== undefined) {
      manualSpeed.value = formatNumber(values[props.manualSpeedKey]);
    }
  } catch (error) {
    console.error("读取初始索引值失败", error);
  }
};

// 读取实时状态值（位置、速度、JOG速度）- 不包含示教定位号和手动定位号
const fetchStatusValues = async () => {
  if (!apiBase) return;
  const actions = [];
  if (props.positionKey) actions.push(props.positionKey);
  if (props.speedKey) actions.push(props.speedKey);
  if (props.jogSpeedKey) actions.push(props.jogSpeedKey);
  if (!actions.length) return;
  try {
    const response = await fetch(`${apiBase}/api/registers/read`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ actions }),
    });
    if (!response.ok) return;
    const data = await response.json();
    const values = data.values || {};
    if (props.positionKey && values[props.positionKey] !== undefined) {
      positionValue.value = formatNumber(values[props.positionKey]);
    }
    if (props.speedKey && values[props.speedKey] !== undefined) {
      speedValue.value = formatNumber(values[props.speedKey]);
    }
    if (props.jogSpeedKey && values[props.jogSpeedKey] !== undefined) {
      jogSpeed.value = formatNumber(values[props.jogSpeedKey]);
    }
  } catch (error) {
    console.error("读取轴状态失败", error);
  }
};

const timers = [];

onMounted(() => {
  fetchPointValues();
  fetchInitialIndexValues(); // 只在挂载时读取一次示教定位号和手动定位号
  fetchStatusValues();
  // 周期刷新当前位置和当前速度（不包含示教定位号和手动定位号）
  if (props.positionKey || props.speedKey) {
    timers.push(setInterval(fetchStatusValues, 1000));
  }
});

onUnmounted(() => {
  timers.forEach((t) => clearInterval(t));
});
</script>

