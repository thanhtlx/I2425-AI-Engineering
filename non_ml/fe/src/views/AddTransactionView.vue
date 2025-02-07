<template>
  <div class="transaction-form-container">
    <div class="transaction-form-card">
      <h2 class="form-title">Create New Transaction</h2>
      <form @submit.prevent="submitTransaction" class="transaction-form">
        <div class="form-section">
          <h3 class="section-title">Basic Information</h3>
          <div class="form-grid">
            <div class="form-group">
              <label>Transaction Time</label>
              <input type="datetime-local" v-model="formData.transaction_time" required class="form-input">
            </div>
            <div class="form-group">
              <label>User</label>
              <div class="selectable-field" @click="showUserList = !showUserList">
                {{ formData.user_id ? `Selected User: ${formData.user_id}` : 'Select a User' }}
              </div>
              <div v-if="showUserList" class="selectable-list">
                <div v-if="loadingUsers" class="loading">Loading users...</div>
                <div v-else class="list-container">
                  <div 
                    v-for="user in users" 
                    :key="user.id"
                    class="list-item"
                    @click="selectUser(user)"
                  >
                    <div class="user-info">
                      <span class="user-id">ID: {{ user.id }}</span>
                      <span class="user-name">{{ user.first_name }} {{ user.last_name }}</span>
                      <span class="user-email">{{ user.email }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Merchant</label>
              <div class="selectable-field" @click="showMerchantList = !showMerchantList">
                {{ formData.merchant_id ? `Selected Merchant: ${formData.merchant_id}` : 'Select a Merchant' }}
              </div>
              <div v-if="showMerchantList" class="selectable-list">
                <div v-if="loadingMerchants" class="loading">Loading merchants...</div>
                <div v-else class="list-container">
                  <div 
                    v-for="merchant in merchants" 
                    :key="merchant.id"
                    class="list-item"
                    @click="selectMerchant(merchant)"
                  >
                    <div class="merchant-info">
                      <span class="merchant-id">ID: {{ merchant.id }}</span>
                      <span class="merchant-name">{{ merchant.name }}</span>
                      <span class="merchant-category">{{ formatSnakeCase(merchant.merchant_category) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Amount ($)</label>
              <input type="number" step="0.01" v-model="formData.amount" required class="form-input">
            </div>
            <div class="form-group">
              <label>Credit Card</label>
              <div 
                class="selectable-field" 
                :class="{ 'disabled': isCreditCardDisabled }"
                @click="!isCreditCardDisabled && (showCreditCardList = !showCreditCardList)"
              >
                {{ formData.credit_card_id ? 
                  `Selected Card: ****${creditCards.find(card => card.id === formData.credit_card_id)?.number.slice(-4)}` : 
                  'Select a Credit Card' 
                }}
              </div>
              <div v-if="showCreditCardList" class="selectable-list">
                <div v-if="creditCards.length === 0" class="loading">No credit cards found</div>
                <div v-else class="list-container">
                  <div 
                    v-for="card in creditCards" 
                    :key="card.id"
                    class="list-item"
                    @click="selectCreditCard(card)"
                  >
                    <div class="card-info">
                      <span 
                        class="clickable-card" 
                        @click.stop="toggleCardVisibility(card)"
                      >
                        {{ card.showFull ? card.number : `****${card.number.slice(-4)}` }}
                      </span>
                      <span v-if="card.showFull" class="card-id">(ID: {{ card.id }})</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3 class="section-title">Location Information</h3>
          <div class="form-grid">
            <div class="location-group">
              <h4 class="location-title">User Coordinates</h4>
              <div class="form-group">
                <label>Latitude</label>
                <input type="number" step="0.000001" v-model="formData.user_coordinate.latitude" required class="form-input">
              </div>
              <div class="form-group">
                <label>Longitude</label>
                <input type="number" step="0.000001" v-model="formData.user_coordinate.longitude" required class="form-input">
              </div>
            </div>
            <div class="location-group">
              <h4 class="location-title">Merchant Coordinates</h4>
              <div class="form-group">
                <label>Latitude</label>
                <input type="number" step="0.000001" v-model="formData.merchant_coordinate.latitude" required class="form-input">
              </div>
              <div class="form-group">
                <label>Longitude</label>
                <input type="number" step="0.000001" v-model="formData.merchant_coordinate.longitude" required class="form-input">
              </div>
            </div>
          </div>
        </div>

        <button type="submit" class="submit-button">
          Create Transaction
          <span class="button-icon">→</span>
        </button>
      </form>
    </div>
  </div>

  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <button class="modal-close" @click="closeModal">&times;</button>
      
      <div v-if="createdTransaction.is_fraud" class="fraud-warning">
        ⚠️ Warning: This transaction has been flagged as potentially fraudulent!
      </div>

      <h2>Transaction Created Successfully</h2>
      <div v-if="createdTransaction" class="transaction-details">
        <div class="detail-group">
          <h3>Transaction Information</h3>
          <p><strong>ID:</strong> {{ createdTransaction.id }}</p>
          <p><strong>Time:</strong> {{ new Date(createdTransaction.transaction_time).toLocaleString() }}</p>
          <p><strong>Number:</strong> {{ createdTransaction.transaction_number }}</p>
          <p><strong>Amount:</strong> {{ new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(createdTransaction.amount) }}</p>
          <p><strong>Status:</strong> 
            <span class="status-badge" :class="{ 
              'fraud': createdTransaction.is_fraud === true,
              'unidentified': createdTransaction.is_fraud === null,
              'valid': createdTransaction.is_fraud === false
            }">
              {{ createdTransaction.is_fraud === true ? 'Fraudulent' : createdTransaction.is_fraud === false ? 'Valid' : 'Unidentified' }}
            </span>
          </p>
        </div>

        <div class="detail-group">
          <h3>Customer Information</h3>
          <p><strong>Name:</strong> {{ createdTransaction.user_first_name }} {{ createdTransaction.user_last_name }}</p>
          <p>
            <strong>Gender:</strong> 
            <span class="gender-tag" :class="getGenderColor(createdTransaction.user_gender)">
              {{ formatGender(createdTransaction.user_gender) }}
            </span>
          </p>
          <p><strong>DOB:</strong> {{ formatDate(createdTransaction.user_dob) }}</p>
          <p>
            <strong>Card:</strong> 
            <span 
              @click="toggleCardVisibility" 
              class="card-number"
              :title="showFullCard ? 'Click to hide' : 'Click to reveal'"
            >
              {{ showFullCard ? createdTransaction.credit_card_number : `****${createdTransaction.credit_card_number.slice(-4)}` }}
            </span>
          </p>
        </div>

        <div class="detail-group">
          <h3>Location Information</h3>
          <p><strong>Merchant:</strong> {{ createdTransaction.merchant_name }}</p>
          <p><strong>Category:</strong> {{ formatSnakeCase(createdTransaction.merchant_category) }}</p>
          <p><strong>Customer Address:</strong><br>
            {{ createdTransaction.user_street }}<br>
            {{ createdTransaction.user_city }}, {{ createdTransaction.user_state }} {{ createdTransaction.user_zip }}</p>
          <p><strong>City Population:</strong> {{ createdTransaction.city_population.toLocaleString() }}</p>
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
      formData: {
        transaction_time: '',
        credit_card_id: 0,
        merchant_id: 0,
        amount: 0.00,
        user_id: 0,
        user_coordinate: {
          latitude: 0.00,
          longitude: 0.00
        },
        merchant_coordinate: {
          latitude: 0.00,
          longitude: 0.00
        }
      },
      users: [],
      merchants: [],
      loadingUsers: false,
      loadingMerchants: false,
      showUserList: false,
      showMerchantList: false,
      creditCards: [],
      showCreditCardList: false,
      showModal: false,
      createdTransaction: null,
      showFullCard: false,
      isCreditCardDisabled: true
    };
  },
  methods: {
    async submitTransaction() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch('/api/transaction', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.formData)
        });

        if (!response.ok) {
          throw new Error('Failed to create transaction');
        }

        const result = await response.json();
        this.createdTransaction = result;
        this.showModal = true;
      } catch (error) {
        console.error('Error:', error);
        alert('Error creating transaction');
      }
    },
    async fetchUsers() {
      this.loadingUsers = true;
      try {
        const response = await axios.get('/api/users');
        this.users = response.data.items;
      } catch (error) {
        console.error('Error fetching users:', error);
      } finally {
        this.loadingUsers = false;
      }
    },
    async fetchMerchants() {
      this.loadingMerchants = true;
      try {
        const response = await axios.get('/api/merchants');
        this.merchants = response.data.items;
      } catch (error) {
        console.error('Error fetching merchants:', error);
      } finally {
        this.loadingMerchants = false;
      }
    },
    selectUser(user) {
      this.formData.user_id = user.id;
      this.showUserList = false;
      this.onUserSelect(user.id);
    },
    async fetchUserCreditCards(userId) {
      try {
        const token = localStorage.getItem('authToken');
        const response = await axios.get(`/api/users/${userId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.creditCards = response.data.credit_cards.map(card => ({
          ...card,
          showFull: false
        }));
        
        // Prefill if only one card exists
        if (this.creditCards.length === 1) {
          this.formData.credit_card_id = this.creditCards[0].id;
        }
      } catch (error) {
        console.error('Error fetching credit cards:', error);
      }
    },
    toggleCardVisibility(card) {
      card.showFull = !card.showFull;
    },
    selectCreditCard(card) {
      this.formData.credit_card_id = card.id;
      this.showCreditCardList = false;
    },
    selectMerchant(merchant) {
      this.formData.merchant_id = merchant.id;
      this.showMerchantList = false;
    },
    closeModal() {
      this.showModal = false;
      this.createdTransaction = null;
    },
    toggleCardVisibility() {
      this.showFullCard = !this.showFullCard;
    },
    formatGender(gender) {
      return gender === 'M' ? 'Male' : gender === 'F' ? 'Female' : gender;
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    getGenderColor(gender) {
      switch (gender) {
        case 'M': return 'blue';
        case 'F': return 'pink';
        default: return 'gray';
      }
    },
    formatSnakeCase(text) {
      return text
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
    },
    onUserSelect(userId) {
      this.isCreditCardDisabled = false;
      this.fetchUserCreditCards(userId);
    }
  },
  mounted() {
    this.fetchUsers();
    this.fetchMerchants();
  }
};
</script>

<style scoped>
.transaction-form-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem;
}

.transaction-form-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.form-title {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 600;
}

.form-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 10px;
}

.section-title {
  color: #34495e;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  font-weight: 500;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.location-group {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.location-title {
  color: #34495e;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #42b983;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
  outline: none;
}

.submit-button {
  background: linear-gradient(135deg, #42b983 0%, #3aa876 100%);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  transition: all 0.3s ease;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(66, 185, 131, 0.2);
}

.button-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.submit-button:hover .button-icon {
  transform: translateX(3px);
}

.selectable-field {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  background-color: white;
  transition: all 0.3s ease;
}

.selectable-field:hover {
  border-color: #42b983;
}

.selectable-list {
  position: absolute;
  z-index: 100;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  max-height: 300px;
  overflow-y: auto;
  width: 100%;
  margin-top: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.list-container {
  padding: 0.5rem;
}

.list-item {
  padding: 0.8rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.list-item:hover {
  background-color: #f5f5f5;
}

.user-info, .merchant-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.user-id, .merchant-id {
  font-size: 0.8rem;
  color: #666;
}

.user-name, .merchant-name {
  font-weight: 500;
}

.user-email, .merchant-category {
  font-size: 0.9rem;
  color: #444;
}

.loading {
  padding: 1rem;
  text-align: center;
  color: #666;
}

.card-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.clickable-card {
  cursor: pointer;
}

.card-id {
  font-size: 0.8rem;
  color: #666;
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

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.fraud {
  background-color: #E91E63;
  color: white;
}

.status-badge.unidentified {
  background-color: #6c757d;
  color: white;
}

.status-badge.valid {
  background-color: #4CAF50;
  color: white;
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

.fraud-warning {
  background-color: #fff3e0;
  border: 1px solid #ff9800;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  color: #e65100;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: pulseWarning 1.5s infinite;
}

@keyframes pulseWarning {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 152, 0, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 152, 0, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 152, 0, 0);
  }
}

.selectable-field.disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
