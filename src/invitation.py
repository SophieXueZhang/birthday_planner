"""
邀请函生成模块
"""
from models import Party, Guest


class InvitationGenerator:
    """邀请函生成器"""

    @staticmethod
    def generate_text_invitation(party: Party, guest: Guest) -> str:
        """生成文本格式的邀请函"""
        invitation = f"""
╔══════════════════════════════════════════════════════════════╗
║                     生日派对邀请函                           ║
╚══════════════════════════════════════════════════════════════╝

亲爱的 {guest.name}，

我们诚挚地邀请您参加 {party.child_name} 的 {party.child_age} 岁生日派对！

【派对详情】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  小寿星：{party.child_name}
  年    龄：{party.child_age} 岁
  日    期：{party.party_date}
  时    间：{party.party_time}
  地    点：{party.venue}
  地    址：{party.venue_address}
"""
        if party.theme:
            invitation += f"  主    题：{party.theme}\n"

        invitation += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

期待您的光临，让我们一起为 {child_name} 庆祝这个特别的日子！

请回复确认是否能够参加。

敬请期待！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
联系方式：{contact}
""".format(child_name=party.child_name, contact=guest.contact)

        return invitation

    @staticmethod
    def generate_html_invitation(party: Party, guest: Guest) -> str:
        """生成HTML格式的邀请函"""
        theme_color = "#FF6B9D"  # 粉色主题

        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{party.child_name}的生日派对邀请函</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
        }}
        .invitation {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: {theme_color};
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 32px;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 18px;
            opacity: 0.9;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 18px;
            margin-bottom: 20px;
            color: #333;
        }}
        .details {{
            background: #f8f9fa;
            border-left: 4px solid {theme_color};
            padding: 20px;
            margin: 20px 0;
        }}
        .detail-item {{
            margin: 12px 0;
            display: flex;
        }}
        .detail-label {{
            font-weight: bold;
            color: {theme_color};
            min-width: 80px;
        }}
        .detail-value {{
            color: #333;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
        }}
        .emoji {{
            font-size: 50px;
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="invitation">
        <div class="header">
            <h1>🎉 生日派对邀请函 🎉</h1>
            <p>{party.child_name} 的 {party.child_age} 岁生日派对</p>
        </div>
        <div class="content">
            <div class="greeting">
                亲爱的 <strong>{guest.name}</strong>，
            </div>
            <p>我们诚挚地邀请您参加 <strong>{party.child_name}</strong> 的 <strong>{party.child_age}</strong> 岁生日派对！</p>

            <div class="emoji">🎂🎈🎁</div>

            <div class="details">
                <h3 style="margin-top:0; color: {theme_color};">派对详情</h3>
                <div class="detail-item">
                    <span class="detail-label">小寿星：</span>
                    <span class="detail-value">{party.child_name}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">年龄：</span>
                    <span class="detail-value">{party.child_age} 岁</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">日期：</span>
                    <span class="detail-value">{party.party_date}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">时间：</span>
                    <span class="detail-value">{party.party_time}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">地点：</span>
                    <span class="detail-value">{party.venue}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">地址：</span>
                    <span class="detail-value">{party.venue_address}</span>
                </div>
"""
        if party.theme:
            html += f"""
                <div class="detail-item">
                    <span class="detail-label">主题：</span>
                    <span class="detail-value">{party.theme}</span>
                </div>
"""

        html += f"""
            </div>

            <p style="margin-top: 30px; text-align: center; font-size: 16px; color: #666;">
                期待您的光临，让我们一起为 {party.child_name} 庆祝这个特别的日子！<br>
                请回复确认是否能够参加。
            </p>
        </div>
        <div class="footer">
            联系方式：{guest.contact}
        </div>
    </div>
</body>
</html>
"""
        return html

    @staticmethod
    def save_invitation(invitation: str, filepath: str):
        """保存邀请函到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(invitation)
