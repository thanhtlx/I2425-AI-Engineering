<template>
  <div class="export-data-view">
    <h1>Export Transactions</h1>
    
    <div class="date-filters">
      <label for="from-date">From Date:</label>
      <input 
        type="date" 
        id="from-date" 
        v-model="fromDate" 
        :max="toDate || maxDate"
      />
      
      <label for="to-date">To Date:</label>
      <input 
        type="date" 
        id="to-date" 
        v-model="toDate" 
        :min="fromDate" 
        :max="maxDate"
      />
    </div>
    
    <button @click="exportData" :disabled="!isFormValid || isPolling">
      {{ buttonText }}
    </button>
    
    <div v-if="statusMessage" class="status-message" :class="statusClass">
      {{ statusMessage }}
    </div>
    
    <div v-if="isPolling" class="progress-bar">
      <div class="progress" :style="{ width: progress + '%' }"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      fromDate: '',
      toDate: '',
      maxDate: new Date().toISOString().split('T')[0],
      isPolling: false,
      progress: 0,
      pollInterval: null,
      buttonText: 'Export & Build',
      statusMessage: '',
      statusClass: '',
      shouldPoll: false
    };
  },
  computed: {
    isFormValid() {
      return this.fromDate && this.toDate && this.fromDate <= this.toDate;
    }
  },
  methods: {
    async exportData() {
      try {
        const payload = {
          from_date: new Date(this.fromDate).toISOString(),
          to_date: new Date(this.toDate).toISOString()
        };
        
        await axios.post('/api/export-transactions', payload);
        this.toast.info('Triggering...', { timeout: 2000 });
        this.shouldPoll = true;
        localStorage.setItem('shouldPoll', 'true');
        this.startPolling();
        
      } catch (error) {
        console.error('Export failed:', error);
        this.statusMessage = 'Export failed';
        this.statusClass = 'error';
      }
    },
    async checkExportStatus() {
      try {
        console.log('Checking export status...');
        const response = await axios.get('/api/latest-export-task');
        const { status, progress } = response.data;
        console.log('Status:', status, 'Progress:', progress);
        
        this.progress = progress;
        
        if (status === 'in_progress') {
          this.isPolling = true;
          this.buttonText = 'Exporting...';
          this.statusMessage = `Exporting... ${progress}% complete`;
          this.statusClass = 'in-progress';
        } else {
          this.stopPolling();
          if (status === 'completed') {
            this.statusMessage = 'Export completed successfully';
            this.statusClass = 'success';
            this.buttonText = 'Export Completed';
          } else if (status === 'failed') {
            this.statusMessage = 'Export failed';
            this.statusClass = 'error';
            this.buttonText = 'Export Failed';
          }
          this.shouldPoll = false;
          localStorage.removeItem('shouldPoll');
        }
      } catch (error) {
        console.error('Status check failed:', error);
        this.statusMessage = 'Error checking status, retrying...';
        this.statusClass = 'error';
        if (this.shouldPoll) {
          setTimeout(() => this.checkExportStatus(), 5000);
        }
      }
    },
    startPolling() {
      console.log('Starting polling...');
      this.isPolling = true;
      this.checkExportStatus();
      this.pollInterval = setInterval(() => {
        if (this.shouldPoll) {
          this.checkExportStatus();
        }
      }, 5000);
    },
    stopPolling() {
      console.log('Stopping polling...');
      this.isPolling = false;
      if (this.pollInterval) {
        clearInterval(this.pollInterval);
        this.pollInterval = null;
      }
    }
  },
  mounted() {
    console.log('Component mounted');
    const shouldPoll = localStorage.getItem('shouldPoll') === 'true';
    if (shouldPoll) {
      this.shouldPoll = true;
      this.startPolling();
    }
    this.checkExportStatus();
  },
  beforeUnmount() {
    console.log('Component unmounting');
    if (this.shouldPoll) {
      console.log('Continuing polling in background');
    }
  }
};
</script>

<style scoped>
.export-data-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.date-filters {
  margin: 20px 0;
  display: flex;
  gap: 20px;
  align-items: center;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.status-message {
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.status-message.success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-message.error {
  background-color: #ffebee;
  color: #c62828;
}

.status-message.in-progress {
  background-color: #fff3e0;
  color: #ef6c00;
}

.progress-bar {
  margin-top: 10px;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #42b983;
  transition: width 0.3s ease;
}

button.completed {
  background-color: #42b983;
}

button.failed {
  background-color: #ff4444;
}
</style>
