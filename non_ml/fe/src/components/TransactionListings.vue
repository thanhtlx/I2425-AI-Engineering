<script setup>
import { RouterLink } from 'vue-router';
import { reactive, defineProps, onMounted, ref, computed } from 'vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import axios from 'axios';

const props = defineProps({
  transactions: {
    type: Array,
    required: true,
    default: () => []
  },
  limit: {
    type: Number,
    required: false
  },
  showButton: {
    type: Boolean,
    default: false
  }
})

const state = reactive({
  loading: false,
  error: null,
  transactions: [],
  pagination: {
    currentPage: 1,
    perPage: 10,
    total: 0
  }
});

const selectedTransaction = ref(null);
const showModal = ref(false);
const showFullCard = ref(false);

const filters = reactive({
  amount_lower: null,
  amount_upper: null,
  transaction_time_lower: null,
  transaction_time_upper: null,
  is_fraud: null
});

onMounted(async () => {
  await fetchTransactions();
});

const fetchTransactions = async (page = 1) => {
  try {
    state.loading = true;
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.NpIh-tHsTo89Aa7v3Ewc2cCKFoEb3XUPnfCDQRabJ_I';
    
    const params = {
      page: page,
      per_page: state.pagination.perPage,
      ...filters
    };

    // Remove null/undefined values from params
    Object.keys(params).forEach(key => 
      params[key] === null && delete params[key]
    );
    
    const response = await axios.get('/api/transactions', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params
    });
    
    state.transactions = response.data.items || [];
    state.pagination.currentPage = response.data.page;
    state.pagination.total = response.data.total;
    console.log('Fetched transactions:', state.transactions);
  } catch (error) {
    state.error = 'Failed to fetch transactions';
    console.error('Error fetching transactions:', error);
    state.transactions = [];
  } finally {
    state.loading = false;
  }
};

const handlePageChange = (newPage) => {
  fetchTransactions(newPage);
};

const formatDateTime = (datetime) => {
  return new Date(datetime).toLocaleString()
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

const maskCreditCard = (cardNumber) => {
  return `****${cardNumber.slice(-4)}`
}

const formatTransactionNumber = (txNumber) => {
  return txNumber.slice(0, 8) + '...'
}

const viewAll = () => {
  emit('view-all')
}

const viewTransactionDetails = async (transactionId) => {
  try {
    state.loading = true;
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.NpIh-tHsTo89Aa7v3Ewc2cCKFoEb3XUPnfCDQRabJ_I';
    
    const response = await axios.get(`/api/transactions/${transactionId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    selectedTransaction.value = response.data;
    showModal.value = true;
  } catch (error) {
    console.error('Error fetching transaction details:', error);
    state.error = 'Failed to fetch transaction details';
  } finally {
    state.loading = false;
  }
};

const closeModal = () => {
  showModal.value = false;
  selectedTransaction.value = null;
};

const formatSnakeCase = (text) => {
  return text
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

const formatGender = (gender) => {
  return gender === 'M' ? 'Male' : gender === 'F' ? 'Female' : gender;
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const getGenderColor = (gender) => {
  switch (gender) {
    case 'M':
      return 'blue';
    case 'F':
      return 'pink';
    default:
      return 'gray';
  }
};

const applyFilters = () => {
  fetchTransactions(1); // Reset to first page when filters change
};

const resetFilters = () => {
  filters.amount_lower = null;
  filters.amount_upper = null;
  filters.transaction_time_lower = null;
  filters.transaction_time_upper = null;
  filters.is_fraud = null;
  fetchTransactions(1);
};

const jumpToPage = ref('');
const totalPages = computed(() => 
  Math.ceil(state.pagination.total / state.pagination.perPage)
);

const isValidPageNumber = computed(() => {
  const pageNum = Number(jumpToPage.value);
  return pageNum >= 1 && pageNum <= totalPages.value;
});

const displayedPages = computed(() => {
  const current = state.pagination.currentPage;
  const total = totalPages.value;
  const delta = 2; // Number of pages to show on each side of current page
  
  let pages = [];
  
  if (total <= 7) {
    // If total pages is small, show all pages
    pages = Array.from({ length: total }, (_, i) => i + 1);
  } else {
    // Always include first page
    pages.push(1);
    
    if (current - delta > 2) {
      // Add ellipsis if there's a gap after first page
      pages.push('...');
    }
    
    // Add pages around current page
    for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
      pages.push(i);
    }
    
    if (current + delta < total - 1) {
      // Add ellipsis if there's a gap before last page
      pages.push('...');
    }
    
    // Always include last page
    if (total > 1) {
      pages.push(total);
    }
  }
  
  return pages;
});

const handleJumpToPage = () => {
  if (isValidPageNumber.value) {
    handlePageChange(Number(jumpToPage.value));
    jumpToPage.value = '';
  }
};

const toggleCardVisibility = () => {
  showFullCard.value = !showFullCard.value;
};
</script>

<template>
  <div class="transactions-container">
    <!-- Add Filter Section -->
    <div class="filters-container">
      <div class="filter-group">
        <label>Amount Range:</label>
        <input 
          type="number" 
          v-model="filters.amount_lower" 
          placeholder="Min Amount"
          step="0.01"
        >
        <input 
          type="number" 
          v-model="filters.amount_upper" 
          placeholder="Max Amount"
          step="0.01"
        >
      </div>

      <div class="filter-group">
        <label>Transaction Time Range:</label>
        <input 
          type="datetime-local" 
          v-model="filters.transaction_time_lower"
        >
        <input 
          type="datetime-local" 
          v-model="filters.transaction_time_upper"
        >
      </div>

      <div class="filter-group">
        <label>Transaction Status:</label>
        <select v-model="filters.is_fraud">
          <option :value="null">All</option>
          <option :value="true">Fraudulent</option>
          <option :value="false">Valid</option>
        </select>
      </div>

      <div class="filter-actions">
        <button @click="applyFilters" class="filter-button apply">Apply Filters</button>
        <button @click="resetFilters" class="filter-button reset">Reset</button>
      </div>
    </div>

    <div v-if="state.loading" class="loading-container">
      <PulseLoader :loading="state.loading" color="#007bff" />
    </div>
    
    <div v-else-if="state.error" class="error-message">
      {{ state.error }}
    </div>

    <table v-else class="transactions-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Time</th>
          <th>Transaction Number</th>
          <th>Card Number</th>
          <th>Merchant</th>
          <th>Amount</th>
          <th>Customer</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in state.transactions.slice(0, limit || state.transactions.length)" 
            :key="transaction.id"
            :class="{ 'fraud': transaction.is_fraud }"
            @click="viewTransactionDetails(transaction.id)"
            class="clickable-row">
          <td>{{ transaction.id }}</td>
          <td>{{ formatDateTime(transaction.transaction_time) }}</td>
          <td>{{ formatTransactionNumber(transaction.transaction_number) }}</td>
          <td>{{ maskCreditCard(transaction.credit_card_number) }}</td>
          <td>{{ transaction.merchant_name }}</td>
          <td>{{ formatCurrency(transaction.amount) }}</td>
          <td>{{ `${transaction.user_first_name} ${transaction.user_last_name}` }}</td>
          <td>
            <span class="status-badge" :class="{ 
              'fraud': transaction.is_fraud === true,
              'unidentified': transaction.is_fraud === null 
            }">
              {{ transaction.is_fraud === true ? 'Fraudulent' : transaction.is_fraud === false ? 'Valid' : 'Unidentified' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="!state.loading && !state.error" class="pagination">
      <button 
        :disabled="state.pagination.currentPage === 1"
        @click="handlePageChange(1)"
        class="pagination-button"
        title="First Page"
      >
        &laquo;
      </button>

      <button 
        :disabled="state.pagination.currentPage === 1"
        @click="handlePageChange(state.pagination.currentPage - 1)"
        class="pagination-button"
      >
        &lsaquo;
      </button>
      
      <div class="page-numbers">
        <template v-for="pageNum in displayedPages" :key="pageNum">
          <span 
            v-if="pageNum === '...'" 
            class="ellipsis"
          >
            ...
          </span>
          <button
            v-else
            @click="handlePageChange(pageNum)"
            class="pagination-button page-number"
            :class="{ active: pageNum === state.pagination.currentPage }"
          >
            {{ pageNum }}
          </button>
        </template>
      </div>

      <button 
        :disabled="state.pagination.currentPage >= totalPages"
        @click="handlePageChange(state.pagination.currentPage + 1)"
        class="pagination-button"
      >
        &rsaquo;
      </button>

      <button 
        :disabled="state.pagination.currentPage >= totalPages"
        @click="handlePageChange(totalPages)"
        class="pagination-button"
        title="Last Page"
      >
        &raquo;
      </button>

      <div class="page-jump">
        <input 
          type="number" 
          v-model="jumpToPage" 
          :min="1" 
          :max="totalPages"
          class="page-jump-input"
        >
        <button 
          @click="handleJumpToPage" 
          class="pagination-button"
          :disabled="!isValidPageNumber"
        >
          Go
        </button>
      </div>
    </div>

    <!-- Transaction Details Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">&times;</button>
        
        <h2>Transaction Details</h2>
        <div v-if="selectedTransaction" class="transaction-details">
          <div class="detail-group">
            <h3>Transaction Information</h3>
            <p><strong>ID:</strong> {{ selectedTransaction.id }}</p>
            <p><strong>Time:</strong> {{ formatDateTime(selectedTransaction.transaction_time) }}</p>
            <p><strong>Number:</strong> {{ selectedTransaction.transaction_number }}</p>
            <p><strong>Amount:</strong> {{ formatCurrency(selectedTransaction.amount) }}</p>
            <p><strong>Status:</strong> 
              <span class="status-badge" :class="{ 
                'fraud': selectedTransaction.is_fraud === true,
                'unidentified': selectedTransaction.is_fraud === null 
              }">
                {{ selectedTransaction.is_fraud === true ? 'Fraudulent' : selectedTransaction.is_fraud === false ? 'Valid' : 'Unidentified' }}
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

<style scoped>
.transactions-container {
  width: 100%;
  margin: 20px 0;
  overflow-x: auto;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  min-width: 1000px; /* Ensures table doesn't get too squeezed */
}

.transactions-table th,
.transactions-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.transactions-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  white-space: nowrap;
}

.transactions-table tr:hover {
  background-color: #f5f5f5;
}

.transactions-table tr.fraud {
  background-color: #fff8f8;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.fraud {
  background-color: #dc3545;
  color: white;
}

.status-badge:not(.fraud) {
  background-color: #28a745;
  color: white;
}

.status-badge.unidentified {
  background-color: #6c757d;
  color: white;
}

.view-all-button {
  text-align: center;
  margin-top: 20px;
}

.view-all-button button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.view-all-button button:hover {
  background-color: #0056b3;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.error-message {
  color: #dc3545;
  text-align: center;
  padding: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.pagination-button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  min-width: 40px;
  font-size: 0.9rem;
}

.pagination-button.page-number {
  background-color: #f8f9fa;
  color: #007bff;
  border: 1px solid #007bff;
}

.pagination-button.page-number.active {
  background-color: #007bff;
  color: white;
}

.pagination-button:disabled {
  background-color: #cccccc;
  border-color: #cccccc;
  cursor: not-allowed;
}

.pagination-button:not(:disabled):hover {
  background-color: #0056b3;
  color: white;
}

.ellipsis {
  padding: 8px;
  color: #666;
}

.page-jump {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 1rem;
}

.page-jump-input {
  width: 60px;
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.page-jump-input::-webkit-inner-spin-button,
.page-jump-input::-webkit-outer-spin-button {
  opacity: 1;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background-color: #f0f0f0;
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

.filters-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-weight: 600;
  color: #333;
}

.filter-group input,
.filter-group select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}

.filter-actions {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.filter-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.filter-button.apply {
  background-color: #007bff;
  color: white;
}

.filter-button.apply:hover {
  background-color: #0056b3;
}

.filter-button.reset {
  background-color: #6c757d;
  color: white;
}

.filter-button.reset:hover {
  background-color: #5a6268;
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
</style>
