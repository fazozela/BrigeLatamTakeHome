<template>
  <div class="page">
    <main class="content">
      <div class="hero-text">
        <span class="pill">EU-MERCOSUR · Enters into force May 1, 2026</span>
        <h1>Readiness at the<br>Speed of <em>Trust.</em></h1>
        <p>Quantifying Reliability and Readiness for the Latam-Europe Corridor.</p>
      </div>

      <CompanyScoreWidget company-id="123e4567-e89b-12d3-a456-426614174000" />
    </main>
  </div>
</template>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: #0d1b2e;
  font-family: 'Inter', system-ui, sans-serif;
  color: #ffffff;
  min-height: 100vh;
}
</style>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}


.content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 80px 48px;
  gap: 64px;
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
}

.hero-text {
  max-width: 480px;
}

.pill {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: #00c8d7;
  margin-bottom: 24px;
}

h1 {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -1.5px;
  color: #ffffff;
  margin-bottom: 20px;
}

h1 em {
  font-style: normal;
  color: #00c8d7;
}

.hero-text p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.55);
  line-height: 1.6;
}
</style>
