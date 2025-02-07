<template>
  <div class="customer-view">
    <h2>Customers</h2>
    <div class="table-container">
      <table v-if="users.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Date of Birth</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="user in users" 
            :key="user.id"
            @click="showUserDetails(user.id)"
            class="clickable-row"
          >
            <td>{{ user.id }}</td>
            <td>{{ user.first_name }}</td>
            <td>{{ user.last_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ formatDate(user.dob) }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="loading" class="loading">
        Loading...
      </div>
      <div v-else class="no-data">
        No users found
      </div>
      
      <!-- Add pagination controls -->
      <div v-if="totalPages > 1" class="pagination">
        <button 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)"
        >
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          :disabled="currentPage === totalPages" 
          @click="changePage(currentPage + 1)"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Replace the modal with the new component -->
    <CustomerDetailModal 
      v-if="selectedUser"
      :user="selectedUser"
      @close="selectedUser = null"
    />
  </div>
</template>

<script>
import axios from 'axios'
import CustomerDetailModal from '@/components/CustomerDetailModal.vue'

export default {
  name: 'CustomerView',
  components: {
    CustomerDetailModal
  },
  data() {
    return {
      users: [],
      loading: false,
      currentPage: 1,
      perPage: 10,
      total: 0,
      selectedUser: null,
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.total / this.perPage)
    }
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await axios.get('/api/users', {
          params: {
            page: this.currentPage,
            per_page: this.perPage
          }
        })
        this.users = response.data.items
        this.total = response.data.total
      } catch (error) {
        console.error('Error fetching users:', error)
      } finally {
        this.loading = false
      }
    },
    changePage(page) {
      this.currentPage = page
      this.fetchUsers()
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    async showUserDetails(userId) {
      try {
        const response = await axios.get(`/api/users/${userId}`)
        this.selectedUser = response.data
      } catch (error) {
        console.error('Error fetching user details:', error)
      }
    }
  },
  mounted() {
    this.fetchUsers()
  }
}
</script>

<style scoped>
.customer-view {
  padding: 20px;
}

.table-container {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}

tr:hover {
  background-color: #f5f5f5;
}

.loading, .no-data {
  text-align: center;
  padding: 20px;
  color: #666;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  border-radius: 4px;
}

.pagination button:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: #999;
}

.pagination button:not(:disabled):hover {
  background-color: #f5f5f5;
}

.clickable-row {
  cursor: pointer;
}

.clickable-row:hover {
  background-color: #f0f0f0;
}
</style>
