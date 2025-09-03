from kivymd.app import MDApp
from datetime import datetime
import random
import string
from kivy.lang import Builder

# try Android WhatsApp integration
try:
    from jnius import autoclass, cast
    ANDROID = True
except ImportError:
    ANDROID = False


def generate_username_password(user):
    digits = string.digits
    alpha = string.ascii_letters
    symbols = "!£$%^&£%&"
    mix = digits + alpha + symbols

    password = "".join(random.choice(mix) for _ in range(8))
    username = user + "".join(random.choice(digits + alpha) for _ in range(9))
    return username, password


class PasswordApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file("password.kv")

    def generate_and_save(self):
        user = self.root.ids.name_input.text.strip()
        platform = self.root.ids.platform_input.text.strip()
        phone = self.root.ids.phone_input.text.strip()

        if not user or not platform or not phone:
            self.root.ids.output_label.text = "⚠ Please enter Name, Platform and Phone!"
            return

        username, password = generate_username_password(user)
        message = f"Your new account for {platform}:\nUsername: {username}\nPassword: {password}"

        # Save locally
        filename = f"{platform.lower()}.txt"
        with open(filename, "a") as f:
            f.write(f"[{datetime.now()}]\n")
            f.write(f"Platform: {platform}\nUsername: {username}\nPassword: {password}\nPhone: {phone}\n\n")

        self.root.ids.output_label.text = f"✅ Sent & Saved!\n{message}"

        if ANDROID:
            self.send_to_whatsapp(phone, message)

    def send_to_whatsapp(self, phone, message):
        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")

        intent = Intent(Intent.ACTION_VIEW)
        uri = Uri.parse(f"whatsapp://send?phone={phone}&text={message}")
        intent.setData(uri)

        currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
        currentActivity.startActivity(intent)


if __name__ == "__main__":
    PasswordApp().run()