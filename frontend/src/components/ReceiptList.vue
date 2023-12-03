<template>
  <div>
    <h2>Receipts List</h2>
    <ul>
      <li v-for="receipt in receipts" :key="receipt.id">
        <router-link :to="{ name: 'receipt-detail', params: { id: receipt.id }}">
          <div class="receipt-item">
            <h3>{{ receipt.name }}</h3>
            <p>{{ receipt.description }}</p>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      receipts: [],
    };
  },
  mounted() {
    // Fetch data from your API endpoint
    fetch("http://localhost:8000/api/v1/receipts/")
      .then((response) => response.json())
      .then((data) => {
        this.receipts = data;
      })
      .catch((error) => console.error("Error fetching receipts:", error));
  },
};
</script>

<style scoped>
/* Add simple styles */
ul {
  list-style-type: none;
  padding: 0;
}

.receipt-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  text-align: start;
}

.receipt-item h3 {
  text-align: center; /* Center the receipt name */
  margin-bottom: 8px; /* Optional: add some spacing between name and description */
}

.receipt-item p {
  margin: 0; /* Remove default margin for paragraphs */
}

.receipt-item:hover {
  background-color: #f5f5f5;
}
</style>
