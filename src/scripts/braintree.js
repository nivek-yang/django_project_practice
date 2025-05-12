import dropin from "braintree-web-drop-in"

export const BraintreeForm = () => ({
  async init() {
    const { token } = this.$el.dataset
    const form = this.$el

    if (token) {
      const instance = await dropin.create({
        container: this.$refs.dropin,
        authorization: token,
      })

      form.addEventListener("submit", (e) => {
        e.preventDefault()

        instance.requestPaymentMethod().then(({ nonce }) => {
          this.$refs.nonce.value = nonce
          form.submit()
        })
      })
    }
  },
})