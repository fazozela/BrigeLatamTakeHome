export default defineEventHandler(async (event) => {
  const { scoreServiceUrl } = useRuntimeConfig(event)
  const body = await readBody(event)
  return $fetch(`${scoreServiceUrl}/score`, { method: 'POST', body })
})
