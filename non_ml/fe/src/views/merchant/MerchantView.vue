<template>
  <div class="merchant-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading">Loading...</div>

    <!-- Error State -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Table -->
    <table v-if="!loading && !error" class="merchant-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Category</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="merchant in merchants" 
          :key="merchant.id"
          @click="viewTransactions(merchant.id)"
          class="clickable-row"
        >
          <td>{{ merchant.id }}</td>
          <td>{{ merchant.name }}</td>
          <td>{{ formatCategory(merchant.merchant_category) }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div v-if="!loading && !error" class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
      >
        Previous
      </button>
      
      <span class="page-info">
        Page {{ currentPage }} of {{ totalPages }}
      </span>
      
      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
      >
        Next
      </button>

      <select v-model="itemsPerPage" @change="handlePageSizeChange">
        <option value="10">10 per page</option>
        <option value="20">20 per page</option>
        <option value="50">50 per page</option>
      </select>
    </div>

    <!-- Transactions Modal -->
    <div v-if="showTransactionsModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeTransactionsModal">&times;</span>
        <h3>Transactions for {{ selectedMerchantName }}</h3>
        
        <table class="transactions-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Amount</th>
              <th>User</th>
              <th>Fraud</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="transaction in transactions" 
              :key="transaction.id"
              @click="viewTransactionDetails(transaction.id)"
              class="clickable-row"
            >
              <td>{{ formatDate(transaction.transaction_time) }}</td>
              <td>${{ transaction.amount }}</td>
              <td>{{ transaction.user_first_name }} {{ transaction.user_last_name }}</td>
              <td :class="{
                'fraud-tag': transaction.is_fraud === true, 
                'valid-tag': transaction.is_fraud === false,
                'unknown-tag': transaction.is_fraud === null
              }">
                {{ transaction.is_fraud === null ? 'Unidentified' : transaction.is_fraud ? 'Fraud' : 'Valid' }}
              </td>
            </tr>
          </tbody>
        </table>

        <div class="pagination">
          <button 
            :disabled="transactionsCurrentPage === 1" 
            @click="changeTransactionsPage(transactionsCurrentPage - 1)"
          >
            Previous
          </button>
          <span class="page-info">
            Page {{ transactionsCurrentPage }} of {{ transactionsTotalPages }}
          </span>
          <button 
            :disabled="transactionsCurrentPage === transactionsTotalPages" 
            @click="changeTransactionsPage(transactionsCurrentPage + 1)"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Transaction Details Modal -->
    <div v-if="showTransactionModal" class="modal-overlay" @click="closeTransactionModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeTransactionModal">&times;</button>
        
        <h2>Transaction Details</h2>
        <div v-if="selectedTransaction" class="transaction-details">
          <div class="detail-group">
            <h3>Transaction Information</h3>
            <p><strong>ID:</strong> {{ selectedTransaction.id }}</p>
            <p><strong>Time:</strong> {{ formatDate(selectedTransaction.transaction_time) }}</p>
            <p><strong>Number:</strong> {{ selectedTransaction.transaction_number }}</p>
            <p><strong>Amount:</strong> ${{ selectedTransaction.amount }}</p>
            <p><strong>Status:</strong> 
              <span class="status-badge" :class="{ 
                'fraud': selectedTransaction.is_fraud === true, 
                'valid': selectedTransaction.is_fraud === false,
                'unknown': selectedTransaction.is_fraud === null
              }">
                {{ selectedTransaction.is_fraud === null ? 'Unidentified' : selectedTransaction.is_fraud ? 'Fraudulent' : 'Valid' }}
              </span>
            </p>
          </div>

          <div class="detail-group">
            <h3>Customer Information</h3>
            <p><strong>Name:</strong> {{ selectedTransaction.user_first_name }} {{ selectedTransaction.user_last_name }}</p>
            <p>
              <strong>Gender:</strong> 
              <span class="gender-tag" :class="getGenderColor(selectedTransaction.user_gender)">
                {{ formatGender(selectedTransaction.user_gender) }}
              </span>
            </p>
            <p><strong>DOB:</strong> {{ formatDate(selectedTransaction.user_dob) }}</p>
            <p>
              <strong>Card:</strong> 
              <span 
                @click="toggleCardVisibility" 
                class="card-number"
                :title="showFullCard ? 'Click to hide' : 'Click to reveal'"
              >
                {{ showFullCard ? selectedTransaction.credit_card_number : maskCreditCard(selectedTransaction.credit_card_number) }}
              </span>
            </p>
          </div>

          <div class="detail-group">
            <h3>Location Information</h3>
            <p><strong>Merchant:</strong> {{ selectedTransaction.merchant_name }}</p>
            <p><strong>Category:</strong> {{ formatSnakeCase(selectedTransaction.merchant_category) }}</p>
            <p><strong>Customer Address:</strong><br>
              {{ selectedTransaction.user_street }}<br>
              {{ selectedTransaction.user_city }}, {{ selectedTransaction.user_state }} {{ selectedTransaction.user_zip }}</p>
            <p><strong>City Population:</strong> {{ selectedTransaction.city_population.toLocaleString() }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: false,
      error: null,
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      merchants: [],
      showTransactionsModal: false,
      selectedMerchantId: null,
      selectedMerchantName: '',
      transactions: [],
      transactionsCurrentPage: 1,
      transactionsItemsPerPage: 10,
      transactionsTotalItems: 0,
      selectedTransaction: null,
      showTransactionModal: false,
      showFullCard: false
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    transactionsTotalPages() {
      return Math.ceil(this.transactionsTotalItems / this.transactionsItemsPerPage);
    }
  },
  mounted() {
    this.fetchMerchants();
  },
  methods: {
    async fetchMerchants() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('/api/merchants', {
          params: {
            page: this.currentPage,
            per_page: this.itemsPerPage
          }
        });
        this.merchants = response.data.items;
        this.totalItems = response.data.total;
      } catch (error) {
        this.error = 'Failed to load merchants';
        console.error('Error fetching merchants:', error);
      } finally {
        this.loading = false;
      }
    },
    changePage(newPage) {
      if (newPage >= 1 && newPage <= this.totalPages) {
        this.currentPage = newPage;
        this.fetchMerchants();
      }
    },
    handlePageSizeChange() {
      this.currentPage = 1;
      this.fetchMerchants();
    },
    formatCategory(category) {
      return category.replace('_', ' ').toUpperCase();
    },
    async viewTransactions(merchantId) {
      const merchant = this.merchants.find(m => m.id === merchantId);
      this.selectedMerchantId = merchantId;
      this.selectedMerchantName = merchant.name;
      this.showTransactionsModal = true;
      this.transactionsCurrentPage = 1;
      await this.fetchTransactions();
    },
    async fetchTransactions() {
        
      try {
        const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.NpIh-tHsTo89Aa7v3Ewc2cCKFoEb3XUPnfCDQRabJ_I';
        const response = await axios.get('/api/transactions', {
          params: {
            merchant_id: this.selectedMerchantId,
            page: this.transactionsCurrentPage,
            per_page: this.transactionsItemsPerPage
          },
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.transactions = response.data.items;
        this.transactionsTotalItems = response.data.total;
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    },
    async changeTransactionsPage(newPage) {
      if (newPage >= 1 && newPage <= this.transactionsTotalPages) {
        this.transactionsCurrentPage = newPage;
        await this.fetchTransactions();
      }
    },
    closeTransactionsModal() {
      this.showTransactionsModal = false;
      this.transactions = [];
      this.selectedMerchantId = null;
      this.selectedMerchantName = '';
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
    async viewTransactionDetails(transactionId) {
      try {
        this.loading = true;
        const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.NpIh-tHsTo89Aa7v3Ewc2cCKFoEb3XUPnfCDQRabJ_I';
        const response = await axios.get(`/api/transactions/${transactionId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.selectedTransaction = response.data;
        this.showTransactionModal = true;
      } catch (error) {
        console.error('Error fetching transaction details:', error);
        this.error = 'Failed to fetch transaction details';
      } finally {
        this.loading = false;
      }
    },
    closeTransactionModal() {
      this.showTransactionModal = false;
      this.selectedTransaction = null;
    },
    toggleCardVisibility() {
      this.showFullCard = !this.showFullCard;
    },
    formatSnakeCase(text) {
      return text
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
    },
    formatGender(gender) {
      return gender === 'M' ? 'Male' : gender === 'F' ? 'Female' : gender;
    },
    getGenderColor(gender) {
      switch (gender) {
        case 'M': return 'blue';
        case 'F': return 'pink';
        default: return 'gray';
      }
    },
    maskCreditCard(cardNumber) {
      // Implement your masking logic here
      return '**** **** **** ' + cardNumber.slice(-4);
    }
  }
};
</script>

<style scoped>
.merchant-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.merchant-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.merchant-table th,
.merchant-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.merchant-table th {
  background-color: #f5f5f5;
}

.loading {
  padding: 20px;
  text-align: center;
}

.error {
  color: #dc3545;
  padding: 20px;
  text-align: center;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: #fff;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.pagination select {
  padding: 8px;
  border: 1px solid #ddd;
}

.page-info {
  margin: 0 10px;
}

.clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background-color: #f5f5f5;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 1000px;
  max-height: 80vh;
  overflow-y: auto;
}

.close {
  float: right;
  font-size: 24px;
  cursor: pointer;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.transactions-table th,
.transactions-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.transactions-table th {
  background-color: #f5f5f5;
}

.fraud-tag {
  color: #dc3545;
  font-weight: bold;
}

.valid-tag {
  color: #28a745;
  font-weight: bold;
}

.unknown-tag {
  color: #ffc107;
  font-weight: bold;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
}

.transaction-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.detail-group {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.detail-group h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.1rem;
}

.detail-group p {
  margin: 0.5rem 0;
}

.detail-group strong {
  color: #666;
}

.gender-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
}

.gender-tag.blue {
  background-color: #2196F3;
}

.gender-tag.pink {
  background-color: #E91E63;
}

.gender-tag.gray {
  background-color: #9E9E9E;
}

.card-number {
  cursor: pointer;
  user-select: none;
  padding: 2px 4px;
  background-color: #f0f0f0;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.card-number:hover {
  background-color: #e0e0e0;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
}

.status-badge.fraud {
  background-color: #dc3545;
}

.status-badge.valid {
  background-color: #28a745;
}

.status-badge.unknown {
  background-color: #ffc107;
}
</style>
