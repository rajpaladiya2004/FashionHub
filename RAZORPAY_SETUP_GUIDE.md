# 🔐 Razorpay Integration Complete Setup Guide

## ✅ What's Been Implemented

### 1. **Core Functions Added**
- ✅ `razorpay_payment()` - Creates Razorpay order and displays payment page
- ✅ `razorpay_payment_success()` - Verifies payment signature and processes success
- ✅ `razorpay_payment_cancel()` - Handles payment cancellation
- ✅ `razorpay_webhook()` - Receives webhook notifications from Razorpay
- ✅ `razorpay_refund()` - Admin panel refund functionality

### 2. **URLs Configured**
```python
/razorpay-payment/<order_id>/          # Payment page
/razorpay-payment-success/             # Payment success handler
/razorpay-payment-cancel/<order_id>/   # Payment cancellation
/razorpay-webhook/                     # Webhook endpoint
/admin-panel/orders/<order_id>/refund/ # Admin refund
```

### 3. **Database Fields** (Already in Order model)
- `razorpay_order_id` - Razorpay Order ID
- `razorpay_payment_id` - Payment ID after success
- `razorpay_signature` - Payment signature for verification

### 4. **Admin Panel Features**
- ✅ Refund button in order details (only for PAID orders)
- ✅ Refund modal with amount and reason fields
- ✅ Support for partial and full refunds

---

## 📋 Setup Steps

### Step 1: Install Razorpay SDK
```bash
# Activate your virtual environment first
.venv\Scripts\activate

# Install razorpay
pip install razorpay

# Freeze requirements
pip freeze > requirements.txt
```

### Step 2: Get Razorpay API Keys

1. **Create Razorpay Account**
   - Go to https://dashboard.razorpay.com/
   - Sign up or login

2. **Get Test Keys**
   - Dashboard → Settings → API Keys
   - Click "Generate Test Key"
   - Copy:
     - Key ID (starts with `rzp_test_`)
     - Key Secret

3. **Update `settings.py`**
   ```python
   # Razorpay Payment Gateway Settings
   RAZORPAY_KEY_ID = 'rzp_test_xxxxxxxxxxxxx'
   RAZORPAY_KEY_SECRET = 'your_secret_key_here'
   RAZORPAY_WEBHOOK_SECRET = 'your_webhook_secret'
   ```

### Step 3: Configure Webhooks (Important!)

1. **Go to Razorpay Dashboard**
   - Settings → Webhooks
   - Click "Add New Webhook"

2. **Webhook Configuration**
   - **Webhook URL**: `https://yourdomain.com/razorpay-webhook/`
   - **Secret**: Generate a random string and save it
   - **Events to track**:
     - ☑️ payment.captured
     - ☑️ payment.failed
     - ☑️ refund.created
     - ☑️ refund.processed

3. **Update settings.py with webhook secret**
   ```python
   RAZORPAY_WEBHOOK_SECRET = 'your_webhook_secret_here'
   ```

### Step 4: Update Payment Template (if needed)

Check `Hub/templates/razorpay_payment.html` - it should already be configured.

If missing, the template needs:
```javascript
var options = {
    "key": "{{ razorpay_key }}",
    "amount": "{{ order_amount }}",
    "currency": "INR",
    "name": "FashionHub",
    "order_id": "{{ razorpay_order_id }}",
    "handler": function (response) {
        // Submit payment details to success URL
        document.getElementById('razorpay_payment_id').value = response.razorpay_payment_id;
        document.getElementById('razorpay_signature').value = response.razorpay_signature;
        document.getElementById('payment_form').submit();
    }
};
```

---

## 🧪 Testing

### Test Mode Cards (Use with Test Keys)

| Card Number         | Purpose      | CVV | Expiry  |
|---------------------|--------------|-----|---------|
| 4111 1111 1111 1111 | Success      | 123 | Any     |
| 4000 0000 0000 0002 | Failed       | 123 | Any     |
| 5555 5555 5555 4444 | Success      | 123 | Any     |

### Testing Flow

1. **Test Payment Success**
   ```
   1. Add product to cart
   2. Go to checkout
   3. Select "Razorpay" payment method
   4. Use test card: 4111 1111 1111 1111
   5. Complete payment
   6. Verify order status changed to "PAID"
   ```

2. **Test Payment Failure**
   ```
   1. Checkout with Razorpay
   2. Use test card: 4000 0000 0000 0002
   3. Payment should fail
   4. Order status should be "FAILED"
   ```

3. **Test Refund**
   ```
   1. Login as admin
   2. Go to order details of PAID order
   3. Click "Refund" button
   4. Enter refund amount and reason
   5. Click "Process Refund"
   6. Check Razorpay dashboard for refund status
   ```

---

## 🚀 Production Deployment

### Before Going Live

1. **Get Live API Keys**
   - Razorpay Dashboard → Settings → API Keys
   - Switch to "Live Mode"
   - Generate Live Keys (starts with `rzp_live_`)

2. **Update settings.py with Live Keys**
   ```python
   RAZORPAY_KEY_ID = 'rzp_live_xxxxxxxxxxxxx'
   RAZORPAY_KEY_SECRET = 'live_secret_here'
   RAZORPAY_WEBHOOK_SECRET = 'live_webhook_secret'
   ```

3. **Update Webhook URL**
   - Change webhook URL to production domain
   - `https://yourdomain.com/razorpay-webhook/`

4. **Verify SSL Certificate**
   - Razorpay requires HTTPS in production
   - Ensure your domain has valid SSL

5. **Complete KYC**
   - Submit business documents to Razorpay
   - Required for live payments

### Security Checklist

- ✅ Never commit API keys to Git
- ✅ Use environment variables for production
- ✅ Enable webhook signature verification
- ✅ Use HTTPS in production
- ✅ Store keys in secure environment

---

## 🔧 Advanced Features

### 1. **Partial Refunds**
Admins can refund partial amounts:
```python
# In refund modal, change the amount field
# Default is full amount, but can be reduced
```

### 2. **Webhook Events**
Currently handling:
- `payment.captured` - Payment successful
- `payment.failed` - Payment failed

Can be extended for:
- `refund.created`
- `refund.processed`
- `payment.authorized`

### 3. **Payment Method Support**
Razorpay supports:
- Credit/Debit Cards
- Net Banking
- UPI (Google Pay, PhonePe, etc.)
- Wallets (Paytm, PhonePe, etc.)
- EMI

---

## 📊 Monitoring & Logs

### Check Payment Status
```python
# In Django shell
from Hub.models import Order

# Get order
order = Order.objects.get(order_number='ORD20260129001')

# Check Razorpay details
print(f"Order ID: {order.razorpay_order_id}")
print(f"Payment ID: {order.razorpay_payment_id}")
print(f"Payment Status: {order.payment_status}")
```

### Razorpay Dashboard
- View all transactions
- Download settlement reports
- Track refunds
- Analyze payment success rate

---

## 🐛 Troubleshooting

### Issue: Payment Gateway Not Configured
**Solution**: Add Razorpay keys in `settings.py`

### Issue: Signature Verification Failed
**Solution**: Check if `RAZORPAY_KEY_SECRET` is correct

### Issue: Webhook Not Working
**Solution**: 
- Verify webhook URL is accessible
- Check webhook secret matches
- Ensure webhook endpoint doesn't require CSRF token

### Issue: Refund Failed
**Solution**:
- Verify payment was successful
- Check if payment ID exists
- Ensure sufficient settlement balance in Razorpay

---

## 📞 Support

- **Razorpay Docs**: https://razorpay.com/docs/
- **API Reference**: https://razorpay.com/docs/api/
- **Support**: https://razorpay.com/support/

---

## ✅ Final Checklist

- [ ] Install razorpay package
- [ ] Add API keys to settings.py
- [ ] Test payment success flow
- [ ] Test payment failure flow
- [ ] Test refund functionality
- [ ] Configure webhooks
- [ ] Test webhook events
- [ ] Verify order status updates
- [ ] Check cart clearing after payment
- [ ] Test on production with live keys

---

**🎉 Your Razorpay integration is now complete!**
