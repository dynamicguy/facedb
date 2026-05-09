<script lang="ts" setup>
import type { TableColumn } from '@nuxt/ui'
import { useAuthStore } from '@/stores/auth'

import type { User } from '~/types'

const autStore = useAuthStore()

const UAvatar = resolveComponent('UAvatar')
const UButton = resolveComponent('UButton')

const { data, status } = useLazyFetch<User[]>('/backend/users', {
  key: 'table-users',
  headers: {
    'Authorization': `Bearer ${autStore.token}`,
    'Content-Type': 'application/json'
  },
  transform: (data) => {
    return (
      data?.map(user => ({
        ...user,
        avatar: { src: `https://i.pravatar.cc/120?img=${user.username}`, alt: `${user.full_name} avatar` }
      })) || []
    )
  },
  server: false
})

const columns: TableColumn<User>[] = [
  {
    accessorKey: 'name',
    header: 'Name',
    cell: ({ row }) => {
      return h('div', { class: 'flex items-center gap-3' }, [
        h(UAvatar, {
          ...row.original.avatar,
          loading: 'lazy',
          size: 'lg'
        }),
        h('div', undefined, [
          h('p', { class: 'font-medium text-highlighted' }, row.original.full_name),
          h('p', { class: '' }, `@${row.original.username}`)
        ])
      ])
    }
  },
  {
    accessorKey: 'email',
    header: 'Email'
  },
  {
    accessorKey: 'role',
    header: 'Role',
    cell: ({ row }) => row.original.role
  },
  {
    accessorKey: 'actions',
    header: 'Actions',
    cell: ({ row }) => {
      return h('div', { class: 'flex items-center gap-3' }, [
        h(UButton, {
          icon: 'i-lucide-eye',
          label: 'View',
          color: 'neutral',
          variant: 'outline',
          size: 'sm',
          to: `/users/${row.original.id}`
        }),
        h(UButton, {
          icon: 'i-lucide-edit',
          label: 'Edit',
          color: 'primary',
          variant: 'outline',
          size: 'sm',
          to: `/users/${row.original.id}/edit`
        }),
        h(UButton, {
          icon: 'i-lucide-trash',
          label: 'Delete',
          color: 'error',
          variant: 'outline',
          size: 'sm'
        })
      ])
    }
  }
]
</script>

<template>
  <UDashboardPanel id="users">
    <template #header>
      <UDashboardNavbar title="Users">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <SuspectsAddModal />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <UCard>
        <UTable
          :data="data"
          :columns="columns"
          :loading="status === 'pending' || status === 'idle'"
          class="flex-1 h-80"
        />
      </UCard>
    </template>
  </UDashboardPanel>
</template>
