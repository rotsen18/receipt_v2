<template>
  <div>
    <h2>Receipt Detail</h2>
    <div v-if="receipt">
      <h3>{{ receipt.name }}</h3>
      <p>{{ receipt.description }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      receipt: null,
    };
  },
  mounted() {
    // Fetch data for the selected receipt from your API endpoint
    const receiptId = this.$route.params.id;
    fetch(`http://127.0.0.1:8000/api/v1/receipts/${receiptId}`)
      .then((response) => response.json())
      .then((data) => {
        this.receipt = data;
      })
      .catch((error) => console.error("Error fetching receipt details:", error));
  },
};
</script>

<style scoped>
/* Add simple styles */
h3 {
  color: #333;
}

p {
  color: #666;
}
</style>
