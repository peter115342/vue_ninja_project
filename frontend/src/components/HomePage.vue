<template>
  <div class="home-page">
    <h1>Dashboard</h1>
    <div class="dashboard-content">
      <div class="dashboard-card">
        <h2>Total Users</h2>
        <p class="dashboard-value">1,234</p>
      </div>
      <div class="dashboard-card">
        <h2>Active Projects</h2>
        <p class="dashboard-value">56</p>
      </div>
      <div class="dashboard-card">
        <h2>Revenue</h2>
        <p class="dashboard-value">$98,765</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  // Add any necessary component logic here
}
</script>

<style scoped>
.home-page {
  padding: 20px;
}

.dashboard-content {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.dashboard-card {
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  width: 200px;
}

.dashboard-value {
  font-size: 24px;
  font-weight: bold;
  margin-top: 10px;
}
</style>
