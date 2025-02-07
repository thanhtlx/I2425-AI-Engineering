<template>
  <div class="modal" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Transaction Details</h3>
        <button class="close-button" @click="$emit('close')">&times;</button>
      </div>
      <div class="modal-body">
        <div class="detail-row">
          <strong>Transaction #:</strong> {{ transaction.transaction_number }}
        </div>
        <div class="detail-row">
          <strong>Date:</strong> {{ formatDateTime(transaction.transaction_time) }}
        </div>
        <div class="detail-row">
          <strong>Amount:</strong> 
          <span :class="{'amount-negative': transaction.amount < 0}">
            ${{ transaction.amount.toFixed(2) }}
          </span>
        </div>
        <div class="detail-row">
          <strong>Status:</strong>
          <span class="status-tag" :class="{
            'failed': transaction.is_fraud === true,
            'completed': transaction.is_fraud === false,
            'unknown': transaction.is_fraud === null
          }">
            {{ 
              transaction.is_fraud === true ? 'Fraudulent' : 
              transaction.is_fraud === false ? 'Valid' : 
              'Unidentified' 
            }}
          </span>
        </div>
        
        <h4 class="section-title-merchant">Merchant Information</h4>
        <div class="detail-row">
          <strong>Name:</strong> {{ transaction.merchant_name }}
        </div>
        <div class="detail-row">
          <strong>Category:</strong> {{ formatCategory(transaction.merchant_category) }}
        </div>
        <div class="detail-row">
          <strong>Location:</strong> 
          {{ transaction.merchant_latitude }}, {{ transaction.merchant_longitude }}
        </div>
        
        <h4 class="section-title-customer">Customer Information</h4>
        <div class="detail-row">
          <strong>Name:</strong> {{ transaction.user_first_name }} {{ transaction.user_last_name }}
        </div>
        <div class="detail-row">
          <strong>Address:</strong><br>
          {{ transaction.user_street }}<br>
          {{ transaction.user_city }}, {{ transaction.user_state }} {{ transaction.user_zip }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TransactionDetailModal',
  props: {
    transaction: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString()
    },
    formatCategory(category) {
      return category
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
  }
}
</script>

<style scoped>
/* Reuse the same modal styles from CustomerDetailModal */
.modal {
  background-color: rgba(255, 255, 255, 1);
}

.modal-content {
  background: white;
}

/* Status tag styles */
.status-tag {
  padding: 4px 8px;
  border-radius: 12px;
  color: white;
  font-size: 0.9em;
}

.status-tag.completed {
  background-color: #4CAF50; /* Green for valid */
}

.status-tag.failed {
  background-color: #f44336; /* Red for fraudulent */
}

.status-tag.unknown {
  background-color: #FF9800; /* Orange for unknown */
}

/* Section title styles */
.section-title-merchant {
  color: #1A237E;
  background-color: #E8EAF6;
  padding: 8px;
  border-radius: 4px;
  margin: 16px 0 8px;
}

.section-title-customer {
  color: #4A148C;
  background-color: #F3E5F5;
  padding: 8px;
  border-radius: 4px;
  margin: 16px 0 8px;
}

/* Add any additional styles specific to transaction details */
</style> 