export default defineEventHandler(async (event) => {
  const { scoreServiceUrl } = useRuntimeConfig(event)

  // Guard against an unset/misconfigured `NUXT_SCORE_SERVICE_URL`. Without
  // this, `${scoreServiceUrl}/score` collapses to `/score`, and `$fetch`
  // resolves that as a request to the Nuxt host itself — the proxy can
  // self-loop and the browser gets a 200 with HTML.
  if (!scoreServiceUrl || typeof scoreServiceUrl !== 'string') {
    throw createError({
      statusCode: 500,
      statusMessage: 'SCORE_SERVICE_URL is not configured',
    })
  }

  const body = await readBody(event)

  try {
    return await $fetch(`${scoreServiceUrl}/score`, {
      method: 'POST',
      body,
      timeout: 5000,
      retry: 0,
    })
  } catch (err: any) {
    // Forward the upstream HTTP status so the widget can render meaningful
    // error states (e.g. 422 validation vs 502 upstream-down) instead of
    // a generic 500. Pydantic's `detail` payload is preserved in `data`.
    throw createError({
      statusCode: err?.statusCode ?? 502,
      statusMessage: err?.statusMessage ?? 'Upstream score service error',
      data: err?.data,
    })
  }
})
