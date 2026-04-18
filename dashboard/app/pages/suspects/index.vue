<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { upperFirst } from 'scule'
import type { Row } from '@tanstack/table-core'
import type { SuspectList, Suspect } from '~/types'
import { useAuthStore } from '@/stores/auth'

const UAvatar = resolveComponent('UAvatar')
const UButton = resolveComponent('UButton')
// const UBadge = resolveComponent('UBadge')
const UDropdownMenu = resolveComponent('UDropdownMenu')
const UCheckbox = resolveComponent('UCheckbox')

// definePageMeta({
//   middleware: 'auth'
// })

const autStore = useAuthStore()

const toast = useToast()
const table = useTemplateRef('table')

const columnFilters = ref([{
  id: 'name',
  value: ''
}])

const page = ref(1)
const pageSize = ref(10)
const search = ref('')

const columnVisibility = ref()
const rowSelection = ref({ })

const sort = ref({
  column: 'created_at',
  direction: 'desc'
})

const { data, status, refresh } = await useFetch<SuspectList>('/backend/items', {
  lazy: true,
  headers: {
    'Authorization': `Bearer ${autStore.token}`,
    'Content-Type': 'application/json'
  },
  query: computed(() => ({
    quid: new Date().getTime(),
    page: page.value,
    size: pageSize.value,
    search: search.value,
    sort_by: sort.value.column,
    order: sort.value.direction
  })),
  watch: [page, pageSize, search, sort]
})

function getRowItems(row: Row<Suspect>) {
  return [
    {
      type: 'label',
      label: 'Actions'
    },
    {
      label: 'Copy suspect ID',
      icon: 'i-lucide-copy',
      onSelect() {
        navigator.clipboard.writeText(row.original.id.toString())
        toast.add({
          title: 'Copied to clipboard',
          description: 'Suspect ID copied to clipboard'
        })
      }
    },
    {
      type: 'separator'
    },
    {
      label: 'View suspect details',
      icon: 'i-lucide-list',
      to: `/suspects/${row.original.id}`
    },
    {
      label: 'Update suspect details',
      icon: 'i-lucide-pencil',
      to: `/suspects/${row.original.id}/edit`
    },
    {
      type: 'separator'
    },
    {
      label: 'Delete suspect',
      icon: 'i-lucide-trash',
      color: 'error',
      onSelect() {
        toast.add({
          title: 'Suspect deleted',
          description: 'The suspect has been deleted.'
        })
      }
    }
  ]
}

const columns: TableColumn<Suspect>[] = [
  {
    id: 'select',
    header: ({ table }) =>
      h(UCheckbox, {
        'modelValue': table.getIsSomePageRowsSelected()
          ? 'indeterminate'
          : table.getIsAllPageRowsSelected(),
        'onUpdate:modelValue': (value: boolean | 'indeterminate') =>
          table.toggleAllPageRowsSelected(!!value),
        'ariaLabel': 'Select all'
      }),
    cell: ({ row }) =>
      h(UCheckbox, {
        'modelValue': row.getIsSelected(),
        'onUpdate:modelValue': (value: boolean | 'indeterminate') => row.toggleSelected(!!value),
        'ariaLabel': 'Select row'
      })
  },
  {
    accessorKey: 'name',
    header: ({ column }) => {
      const isSorted = column.getIsSorted()

      return h(UButton, {
        color: 'neutral',
        variant: 'ghost',
        label: 'Name',
        icon: isSorted
          ? isSorted === 'asc'
            ? 'i-lucide-arrow-up-narrow-wide'
            : 'i-lucide-arrow-down-wide-narrow'
          : 'i-lucide-arrow-up-down',
        class: '-mx-2.5',
        onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
      })
    },
    cell: ({ row }) => {
      return h('div', { class: 'flex items-center gap-3' }, [
        h(UAvatar, {
          ...row.original.image_url
            ? { src: row.original.image_url }
            : { fallback: row.original.name.toUpperCase() },
          size: 'lg'
        }),
        h('div', undefined, [
          h('p', { class: 'font-medium text-highlighted' }, row.original.name),
          h('p', { class: '' }, `${row.original.gender}`)
        ])
      ])
    }
  },
  {
    accessorKey: 'gender',
    filterFn: 'equals',
    header: ({ column }) => {
      const isSorted = column.getIsSorted()

      return h(UButton, {
        color: 'neutral',
        variant: 'ghost',
        label: 'Gender',
        icon: isSorted
          ? isSorted === 'asc'
            ? 'i-lucide-arrow-up-narrow-wide'
            : 'i-lucide-arrow-down-wide-narrow'
          : 'i-lucide-arrow-up-down',
        class: '-mx-2.5',
        onClick: () => column.toggleSorting(column.getIsSorted() === 'asc')
      })
    }
  },
  {
    accessorKey: 'location',
    header: 'Location',
    cell: ({ row }) => row.original.birth_place
  },
  {
    accessorKey: 'Date of Birth',
    header: 'Date of Birth',
    cell: ({ row }) => new Date(row.original.dob).toLocaleDateString()
  },
  {
    accessorKey: 'created at',
    header: 'Created At',
    cell: ({ row }) => new Date(row.original.created_at).toLocaleDateString()
  },
  {
    id: 'actions',
    cell: ({ row }) => {
      return h(
        'div',
        { class: 'text-right' },
        h(
          UDropdownMenu,
          {
            content: {
              align: 'end'
            },
            items: getRowItems(row)
          },
          () =>
            h(UButton, {
              icon: 'i-lucide-ellipsis-vertical',
              color: 'neutral',
              variant: 'ghost',
              class: 'ml-auto'
            })
        )
      )
    }
  }
]

const genderFilter = ref('all')

watch(() => genderFilter.value, (newVal) => {
  if (!table?.value?.tableApi) return

  const genderColumn = table.value.tableApi.getColumn('gender')
  if (!genderColumn) return

  if (newVal === 'all') {
    genderColumn.setFilterValue(undefined)
  } else {
    genderColumn.setFilterValue(newVal)
  }
})

// const searchQuery = computed({
//   get: (): string => {
//     return (table.value?.tableApi?.getColumn('name')?.getFilterValue() as string) || ''
//   },
//   set: (value: string) => {
//     table.value?.tableApi?.getColumn('name')?.setFilterValue(value || undefined)
//   }
// })
// const rows = computed(() => data.value?.items ?? [])
const total = computed(() => data.value?.total ?? 0)
</script>

<template>
  <UDashboardPanel id="suspects">
    <template #header>
      <UDashboardNavbar title="Suspects">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <SuspectsAddModal />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="flex flex-wrap items-center justify-between gap-1.5">
        <UInput
          v-model="search"
          class="max-w-sm"
          icon="i-lucide-search"
          placeholder="Filter suspects..."
        >
          <template v-if="search?.length" #trailing>
            <UButton
              color="neutral"
              variant="link"
              size="sm"
              icon="i-lucide-circle-x"
              aria-label="Clear input"
              @click="search = ''"
            />
          </template>
        </UInput>

        <div class="flex flex-wrap items-center gap-1.5">
          <SuspectsDeleteModal :count="table?.tableApi?.getFilteredSelectedRowModel().rows.length">
            <UButton
              v-if="table?.tableApi?.getFilteredSelectedRowModel().rows.length"
              label="Delete"
              color="error"
              variant="subtle"
              icon="i-lucide-trash"
            >
              <template #trailing>
                <UKbd>
                  {{ table?.tableApi?.getFilteredSelectedRowModel().rows.length }}
                </UKbd>
              </template>
            </UButton>
          </SuspectsDeleteModal>

          <USelect
            v-model="genderFilter"
            :items="[
              { label: 'All', value: 'all' },
              { label: 'Man', value: 'Man' },
              { label: 'Woman', value: 'Woman' }
            ]"
            :ui="{ trailingIcon: 'group-data-[state=open]:rotate-180 transition-transform duration-200' }"
            placeholder="Filter gender"
            class="min-w-28"
          />
          <UDropdownMenu
            :items="
              table?.tableApi
                ?.getAllColumns()
                .filter((column: any) => column.getCanHide())
                .map((column: any) => ({
                  label: upperFirst(column.id),
                  type: 'checkbox' as const,
                  checked: column.getIsVisible(),
                  onUpdateChecked(checked: boolean) {
                    table?.tableApi?.getColumn(column.id)?.toggleVisibility(!!checked)
                  },
                  onSelect(e?: Event) {
                    e?.preventDefault()
                  }
                }))
            "
            :content="{ align: 'end' }"
          >
            <UButton
              label="Display"
              color="neutral"
              variant="outline"
              trailing-icon="i-lucide-settings-2"
            />
          </UDropdownMenu>
        </div>
      </div>

      <UTable
        ref="table"
        v-model:column-filters="columnFilters"
        v-model:column-visibility="columnVisibility"
        v-model:row-selection="rowSelection"
        class="shrink-0"
        :data="data?.items"
        :columns="columns"
        :loading="status === 'pending'"
        :ui="{
          base: 'table-fixed border-separate border-spacing-0',
          thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none',
          tbody: '[&>tr]:last:[&>td]:border-b-0',
          th: 'py-2 first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r',
          td: 'border-b border-default',
          separator: 'h-0'
        }"
      />

      <div class="flex items-center justify-between gap-3 border-t border-default pt-4 mt-auto">
        <div class="text-sm text-muted">
          {{ table?.tableApi?.getFilteredSelectedRowModel().rows.length || 0 }} of
          {{ table?.tableApi?.getFilteredRowModel().rows.length || 0 }} row(s) selected.
        </div>

        <div class="flex items-center gap-1.5">
          <UPagination
            v-model="page"
            :total="total"
            :page-count="Math.ceil(total / pageSize)"
            @update:page="(p: number) => page = p"
          />
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
