import { ref } from 'vue'
import { fetchUser, type UserResponse } from './apiFetch'
import type { User } from './apiFetch'

export function useUser(userData: User | null = null) {
  const user = ref<UserResponse | null>(null)
  if (userData) {
    login(userData)
  }

  async function login(userData: User): Promise<void> {
    user.value = await userLogin(userData)
  }

  function logout(): void {
    userLogout()
  }

  function check(): boolean {
    if (getUser() && getUserCreds()) {
      return true
    }
    return false
  }

  function getCreds(): string | null {
    return getUserCreds()
  }

  return { user, login, logout, check, getCreds }
}

export function getAuthCreds(user: User): string {
  return 'Basic ' + btoa(`${user.username}:${user.password}`)
}

async function userLogin(userData: User): Promise<UserResponse | null> {
  let userResponse = null
  const userCreds = getAuthCreds(userData)
  try {
    userResponse = await fetchUser(userCreds)
  } catch (error) {
    if (typeof error !== 'object' || error === null || !('code' in error)) {
      throw new Error(`Uncaught error! ${error}`)
    }
    throw error
  }

  if (userResponse) {
    setUser(userCreds, userResponse)
    return userResponse
  }
  return null
}

function userLogout() {
  localStorage.removeItem('user')
  localStorage.removeItem('userAuthCreds')
}

function setUser(userCreds: string, user: UserResponse): void {
  localStorage.setItem('user', JSON.stringify(user))
  localStorage.setItem('userAuthCreds', userCreds)
}

function getUser(): UserResponse | null {
  const user = localStorage.getItem('user')
  if (user) {
    return JSON.parse(user)
  }
  return null
}

function getUserCreds(): string | null {
  const userCreds = localStorage.getItem('userAuthCreds')
  if (userCreds) {
    return userCreds
  }
  return null
}
