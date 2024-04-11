import type { UserResponse } from './apiFetch'

export function userLogin(userCreds: string, user: UserResponse): void {
  localStorage.setItem('user', JSON.stringify(user))
  localStorage.setItem('userAuthCreds', userCreds)
}

export function userLogout(): void {
  localStorage.removeItem('user')
  localStorage.removeItem('userAuthCreds')
}

export function getUserCreds(): string | null {
  return localStorage.getItem('userAuthCreds')
}

export function getUser(): UserResponse | null {
  const user = localStorage.getItem('user')
  if (user) {
    return JSON.parse(user)
  }
  return null
}
