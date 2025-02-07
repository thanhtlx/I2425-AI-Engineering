<template>
  <div v-if="user" class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3>User Details</h3>
        <button class="close-button" @click="$emit('close')">&times;</button>
      </div>
      <div class="modal-body">
        <div class="detail-row">
          <strong>ID:</strong> {{ user.id }}
        </div>
        <div class="detail-row">
          <strong>Name:</strong> {{ user.first_name }} {{ user.last_name }}
        </div>
        <div class="detail-row">
          <strong>Email:</strong> {{ user.email }}
        </div>
        <div class="detail-row">
          <strong>Date of Birth:</strong> {{ formatDate(user.dob) }}
        </div>
        <div class="detail-row">
          <strong>Gender:</strong>
          <span 
            class="gender-tag" 
            :class="user.gender === 'M' ? 'male' : 'female'"
          >
            {{ user.gender === 'M' ? 'Male' : 'Female' }}
          </span>
        </div>
        <div class="detail-row">
          <strong>Job:</strong> {{ user.job }}
        </div>
        <div class="detail-row">
          <strong>Address:</strong><br>
          {{ user.street }}<br>
          {{ user.city }}, {{ user.state }} {{ user.zip }}
        </div>

        <!-- Credit Cards Section -->
        <div class="credit-cards-section">
          <h4>Credit Cards</h4>
          <table v-if="user.credit_cards.length" class="cards-table">
            <thead>
              <tr>
                <th>Card Number</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="card in user.credit_cards" :key="card.id">
                <td>
                  <span 
                    class="clickable-card" 
                    @click="toggleCardVisibility(card)"
                  >
                    {{ card.showFull ? card.number : maskCardNumber(card.number) }}
                  </span>
                  <span v-if="card.showFull" class="card-id">(ID: {{ card.id }})</span>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="no-cards">No credit cards on file</div>
        </div>

        <!-- Transactions Section -->
        <div class="transactions-section">
          <h4>Transaction History</h4>
          <div v-if="loading" class="loading">Loading transactions...</div>
          <div v-else-if="error" class="error">{{ error }}</div>
          <table v-else class="transactions-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Merchant</th>
                <th>Card Number</th>
                <th>Amount</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="transaction in transactions" 
                :key="transaction.id"
                @click="showTransactionDetails(transaction.id)"
                class="clickable-row"
              >
                <td>{{ formatDateTime(transaction.transaction_time) }}</td>
                <td>{{ transaction.merchant_name }}</td>
                <td>{{ maskCardNumber(transaction.credit_card_number) }}</td>
                <td :class="{'amount-negative': transaction.amount < 0}">
                  ${{ transaction.amount.toFixed(2) }}
                </td>
                <td>
                  <span class="status-tag" :class="{
                    'completed': transaction.is_fraud === false,
                    'failed': transaction.is_fraud === true,
                    'unknown': transaction.is_fraud === null
                  }">
                    {{ 
                      transaction.is_fraud === false ? 'Valid' : 
                      transaction.is_fraud === true ? 'Fraudulent' : 
                      'Unidentified' 
                    }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Transaction Detail Modal -->
  <transaction-detail-modal
    v-if="selectedTransaction"
    :transaction="selectedTransaction"
    @close="selectedTransaction = null"
  />
</template>

<script>
import TransactionDetailModal from './CustomerTransactionDetailModal.vue'

export default {
  name: 'CustomerDetailModal',
  components: {
    TransactionDetailModal
  },
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      transactions: [],
      loading: false,
      error: null,
      selectedTransaction: null
    }
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString()
    },
    maskCardNumber(cardNumber) {
      return `****${cardNumber.slice(-4)}`
    },
    async fetchTransactions() {
      this.loading = true
      this.error = null
      const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.NpIh-tHsTo89Aa7v3Ewc2cCKFoEb3XUPnfCDQRabJ_I';
      try {
        const response = await fetch(`/api/transactions?user_id=${this.user.id}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        if (!response.ok) throw new Error('Failed to fetch transactions')
        const data = await response.json()
        this.transactions = data.items
      } catch (err) {
        this.error = 'Failed to load transactions'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async showTransactionDetails(transactionId) {
      try {
        const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.NpIh-tHsTo89Aa7v3Ewc2cCKFoEb3XUPnfCDQRabJ_I';
        const response = await fetch(`/api/transactions/${transactionId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        if (!response.ok) throw new Error('Failed to fetch transaction details')
        const data = await response.json()
        this.selectedTransaction = data
      } catch (err) {
        console.error(err)
        // Optionally show an error message to the user
      }
    },
    toggleCardVisibility(card) {
      card.showFull = !card.showFull;
    }
  },
  mounted() {
    this.fetchTransactions()
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  color: #666;
}

.close-button:hover {
  color: #333;
}

.detail-row {
  margin-bottom: 12px;
  line-height: 1.4;
}

.detail-row strong {
  display: inline-block;
  width: 120px;
  color: #666;
}

.gender-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9em;
  font-weight: 500;
}

.gender-tag.male {
  background-color: #e1f5fe;
  color: #0288d1;
}

.gender-tag.female {
  background-color: #fce4ec;
  color: #d81b60;
}

.credit-cards-section {
  margin-top: 24px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.cards-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}

.cards-table th,
.cards-table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.cards-table th {
  font-weight: 600;
  color: #666;
}

.no-cards {
  color: #666;
  text-align: center;
  padding: 10px;
}

.transactions-section {
  margin-top: 24px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.transactions-section h4 {
  margin-bottom: 16px;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}

.transactions-table th,
.transactions-table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.transactions-table th {
  font-weight: 600;
  color: #666;
}

.amount-negative {
  color: #d32f2f;
}

.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.85em;
  font-weight: 500;
}

.status-tag.completed {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-tag.failed {
  background-color: #ffebee;
  color: #c62828;
}

.status-tag.unknown {
  background-color: #fff3e0;
  color: #ef6c00;
}

.loading {
  text-align: center;
  color: #666;
  padding: 20px;
}

.error {
  color: #d32f2f;
  text-align: center;
  padding: 20px;
}

.clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background-color: #f5f5f5;
}

.clickable-card {
  cursor: pointer;
  color: #2196F3;
  text-decoration: underline;
}

.clickable-card:hover {
  color: #1976D2;
}

.card-id {
  margin-left: 8px;
  color: #666;
  font-size: 0.9em;
}
</style> 