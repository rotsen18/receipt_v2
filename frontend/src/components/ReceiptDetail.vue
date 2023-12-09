<template>
  <div>
    <router-link :to="{ name: 'receipt-list'}">
      <div>
        <h3>All receipts</h3>
      </div>
    </router-link>
    <div v-if="receipt">
      <h2 class="receipt-title">{{ receipt.name }}</h2>
      <h3 v-if="receipt.category">Категорія: {{ receipt.category.name }}</h3>
      <h3 v-if="receipt.cooking_type">Принцип приготування: {{ receipt.cooking_type.name }}</h3>
      <p>{{ receipt.description }}</p>
      <p>{{ receipt.amount }}</p>
      <ul class="component-items">
        <li v-for="component in receipt.components" :key="component.id">
          <div>
            {{ component.ingredient.name }} - {{ component.amount }} {{ component.unit.symbol }}
          </div>
        </li>
      </ul>
      <div class="receipt-procedure">{{ receipt.procedure }}</div>
    </div>
    <div v-else-if="receipt === null">
      <p>Receipt not found.</p>
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
    const receiptId = this.$route.params.id;
    if (receiptId) {
      this.fetchReceiptDetails(receiptId);
    } else {
      console.error("Receipt ID is undefined or null.");
    }
  },
  methods: {
    fetchReceiptDetails(receiptId) {
      const backendUrl = process.env.VUE_APP_BACKEND_SERVER_URL;
      const apiUrl = `${backendUrl}/api/v1/receipts/${receiptId}/`;

      this.fetchApiData(apiUrl)
        .then((receiptData) => {
          this.receipt = receiptData;

          const categoryUrl = `${backendUrl}/api/v1/directory/culinary_categories/${receiptData.category_id}/`;
          this.fetchApiData(categoryUrl)
            .then((categoryData) => {
              this.receipt.category = categoryData;
            });

          const cookingTypeUrl = `${backendUrl}/api/v1/directory/cooking_types/${receiptData.cooking_type_id}/`;
          this.fetchApiData(cookingTypeUrl)
            .then((cookingTypeData) => {
              this.receipt.cooking_type = cookingTypeData;
            });
        })
        .catch((error) => console.error("Error fetching receipt details:", error));
    },
    fetchApiData(url) {
      return fetch(url).then((response) => response.json());
    },
  },
};

</script>

<style scoped>
/* Add styles */
.receipt-title {
  text-align: center;
  color: #555; /* Adjust the color as needed */
  margin-bottom: 10px; /* Add spacing if needed */
}

.receipt-procedure {
  color: #666;
  text-align: left;
  margin-left: 10px;
}

h3 {
  color: #333;
}

p {
  color: #666;
}

.component-items {
  /* Add styles for component items if needed */
  text-align: left;
  list-style-type: decimal;
}
</style>
