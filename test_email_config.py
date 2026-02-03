#!/usr/bin/env python
"""Test email configuration for VibeMall"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'FashioHub'))
django.setup()

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

def test_basic_email():
    """Test basic email sending"""
    print("\n🧪 Testing Basic Email Configuration...")
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Email TLS: {settings.EMAIL_USE_TLS}")
    print(f"From Email: {settings.EMAIL_HOST_USER}")
    print(f"Default From: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        result = send_mail(
            subject='🎉 VibeMall Email Test',
            message='Hello! This is a test email from VibeMall.\n\nIf you received this, email configuration is working correctly!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['info.vibemall@gmail.com'],
            fail_silently=False,
        )
        print(f"\n✅ SUCCESS! Email sent successfully (Result: {result})")
        return True
    except Exception as e:
        print(f"\n❌ FAILED! Email error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_html_email():
    """Test HTML email with template"""
    print("\n🧪 Testing HTML Email Configuration...")
    
    try:
        subject = '🎉 VibeMall Order Confirmation Test'
        from_email = settings.EMAIL_HOST_USER
        to_email = 'info.vibemall@gmail.com'
        
        text_content = """
        Test Order Confirmation
        
        Dear Customer,
        
        Thank you for testing VibeMall email system!
        Your email configuration is working correctly.
        
        Best regards,
        VibeMall Team
        """
        
        html_content = """
        <html>
            <body>
                <h2>🎉 Test Order Confirmation</h2>
                <p>Dear Customer,</p>
                <p>Thank you for testing VibeMall email system!</p>
                <p>Your email configuration is working correctly.</p>
                <hr>
                <p><strong>Best regards,</strong><br>VibeMall Team</p>
            </body>
        </html>
        """
        
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        print(f"✅ SUCCESS! HTML email sent successfully")
        return True
    except Exception as e:
        print(f"❌ FAILED! HTML email error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("VibeMall Email Configuration Test")
    print("=" * 60)
    
    basic_result = test_basic_email()
    html_result = test_html_email()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Basic Email: {'✅ PASS' if basic_result else '❌ FAIL'}")
    print(f"  HTML Email:  {'✅ PASS' if html_result else '❌ FAIL'}")
    print("=" * 60 + "\n")
    
    if basic_result and html_result:
        print("✅ All tests passed! Email is configured correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the configuration.")
        sys.exit(1)
