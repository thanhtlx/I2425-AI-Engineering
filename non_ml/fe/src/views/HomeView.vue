<script setup>
import TransactionListings from '@/components/TransactionListings.vue';
</script>

<template>
  <TransactionListings 
  :transactions="yourTransactionsArray"
  :limit="10"
  :showButton="true"
  @view-all="handleViewAll"
/>
</template>
