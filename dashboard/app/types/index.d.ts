import type { AvatarProps } from '@nuxt/ui'

export type UserStatus = 'subscribed' | 'unsubscribed' | 'bounced'
export type SaleStatus = 'paid' | 'failed' | 'refunded'

export interface User {
  id: number
  username: string
  full_name: string
  email: string
  avatar?: AvatarProps
  status: UserStatus
  location: string
  disabled: boolean
  role: string
}

export interface Mail {
  id: number
  unread?: boolean
  from: User
  subject: string
  body: string
  date: string
}

export interface Member {
  name: string
  username: string
  role: 'member' | 'owner'
  avatar: AvatarProps
}

export interface Stat {
  title: string
  icon: string
  value: number | string
  variation: number
  formatter?: (value: number) => string
}

export interface Sale {
  id: string
  date: string
  status: SaleStatus
  email: string
  amount: number
}

export interface Notification {
  id: number
  unread?: boolean
  sender: User
  body: string
  date: string
}

export type Period = 'daily' | 'weekly' | 'monthly'

export interface Range {
  start: Date
  end: Date
}

export interface Suspect {
  id: string
  name: string
  bio: string
  img_path: string
  gender: string
  dob: string // ISO date string
  birth_place: string
  image_url: string
  face_path: string
  identified_age: number
  identified_gender: string
  identified_race: string
  identified_emotion: string
  username: string
  created_at: string // ISO datetime string
}

export interface SuspectList {
  took: number
  total: number
  q: string
  sort_by: string
  sort_order: string
  start: number
  size: number
  items: Suspect[]
}

export interface Identified {
  identified_age: number
  identified_gender: string
  identified_race: string
  identified_emotion: string
}

export interface SearchResult {
  took: number
  total: number
  identified: Identified
  items: Suspect[]
}
