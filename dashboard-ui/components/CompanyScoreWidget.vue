<template>
  <div class="widget">
    <div class="widget-header">
      <span class="eyebrow">Company Health Score</span>
      <span v-if="!pending && data" class="company-id">{{ companyId }}</span>
    </div>

    <template v-if="pending">
      <div class="skeleton score-skeleton" />
      <div class="skeleton badge-skeleton" />
      <div class="divider" />
      <div v-for="n in 5" :key="n" class="skeleton bar-skeleton" />
    </template>

    <template v-else-if="error">
      <div class="error-state">
        <span class="error-icon">⚠</span>
        <p>Failed to load score. Please try again.</p>
      </div>
    </template>

    <template v-else-if="data">
      <div class="score-row">
        <div class="score">{{ data.composite_score.toFixed(1) }}</div>
        <span class="badge" :class="`grade-${data.grade.toLowerCase()}`">{{ data.grade }}</span>
      </div>
      <p class="score-label">Composite Score</p>

      <div class="divider" />

      <div class="dimensions">
        <div v-for="(value, key) in data.dimension_scores" :key="key" class="dimension">
          <div class="dim-top">
            <span class="dim-label">{{ key }}</span>
            <span class="dim-value">{{ value }}<span class="dim-max">/100</span></span>
          </div>
          <div class="bar-track">
            <div class="bar-fill" :style="{ width: value + '%' }" />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
interface ScoreResponse {
  composite_score: number
  grade: string
  dimension_scores: Record<string, number>
}

const props = defineProps<{ companyId: string }>()

const { data, pending, error } = await useFetch<ScoreResponse>('/api/score', {
  method: 'POST',
  body: {
    company_id: props.companyId,
    dimensions: { governance: 80, innovation: 70, operations: 65, finance: 75, sustainability: 72 },
  },
})
</script>

<style scoped>
.widget {
  font-family: 'Inter', system-ui, sans-serif;
  width: 440px;
  padding: 32px;
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.3);
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.eyebrow {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #00c8d7;
}

.company-id {
  font-size: 11px;
  color: #94a3b8;
  font-family: monospace;
}

.score-row {
  display: flex;
  align-items: flex-end;
  gap: 16px;
}

.score {
  font-size: 72px;
  font-weight: 800;
  line-height: 1;
  color: #0d1b2e;
  letter-spacing: -2px;
}

.score-label {
  font-size: 12px;
  color: #94a3b8;
  margin: 6px 0 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}

.grade-a { background: linear-gradient(135deg, #22c55e, #16a34a); }
.grade-b { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.grade-c { background: linear-gradient(135deg, #f59e0b, #d97706); }
.grade-d { background: linear-gradient(135deg, #ef4444, #dc2626); }

.divider {
  height: 1px;
  background: #e2e8f0;
  margin: 24px 0;
}

.dimensions {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.dim-top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 7px;
}

.dim-label {
  font-size: 13px;
  font-weight: 500;
  text-transform: capitalize;
  color: #334155;
}

.dim-value {
  font-size: 13px;
  font-weight: 600;
  color: #0d1b2e;
}

.dim-max {
  font-size: 11px;
  font-weight: 400;
  color: #94a3b8;
}

.bar-track {
  height: 6px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #00c8d7, #0d1b2e);
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.skeleton {
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  border-radius: 8px;
}

.score-skeleton { height: 72px; width: 140px; }
.badge-skeleton { height: 28px; width: 56px; margin-top: 6px; }
.bar-skeleton { height: 32px; margin-bottom: 4px; }

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px 0;
  color: #94a3b8;
}

.error-icon {
  font-size: 28px;
  color: #ef4444;
}

.error-state p {
  font-size: 14px;
  margin: 0;
  color: #64748b;
}
</style>
