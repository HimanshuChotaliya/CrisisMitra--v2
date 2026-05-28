export function requireAuth() {
  const token = localStorage.getItem("accessToken")

  if (!token) {
    window.location.href = "/login.html"
    throw new Error("Not authenticated")
  }

  return token
}

export async function authFetch(url, options = {}) {
  const token = requireAuth()

  const res = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
    }
  })

  if (res.status === 401) {
    localStorage.removeItem("accessToken")
    window.location.href = "/login.html"
    throw new Error("Unauthorized")
  }

  return res
}
