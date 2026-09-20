# 极简工具箱 - 部署指南

## 一、平台选择

### 推荐平台对比

| 平台 | 优点 | 缺点 | 推荐指数 |
|------|------|------|----------|
| **Vercel** | 自动CI/CD、免费套餐宽裕、全球CDN | 需要GitHub账号 | ⭐⭐⭐⭐⭐ |
| **Netlify** | 拖拽部署、自动HTTPS、表单处理 | 免费版有带宽限制 | ⭐⭐⭐⭐⭐ |
| **GitHub Pages** | 完全免费、与代码同仓库 | 无后端支持、自定义域名需配置 | ⭐⭐⭐⭐ |
| **Cloudflare Pages** | 免费CDN、快速部署 | 功能相对简单 | ⭐⭐⭐⭐ |
| **腾讯云COS** | 国内访问快、便宜 | 需要备案 | ⭐⭐⭐ |

### 推荐方案
- **海外用户为主**: Vercel 或 Netlify
- **国内用户为主**: 腾讯云COS + CDN（需备案）或 Cloudflare Pages

---

## 二、Vercel 部署步骤

### 2.1 准备阶段

1. 将项目代码推送到 GitHub
2. 注册/登录 Vercel (https://vercel.com)

### 2.2 部署步骤

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 在项目根目录登录
vercel login

# 3. 部署到生产环境
vercel --prod

# 或部署到预览环境
vercel
```

### 2.3 手动部署（通过 GitHub）

1. 将项目推送到 GitHub 仓库
2. 在 Vercel 控制台点击 "Add New Project"
3. 选择 GitHub 仓库
4. 点击 "Deploy"
5. 等待部署完成，获取访问链接

### 2.4 自定义域名配置

1. 在 Vercel 控制台选择项目 → Settings → Domains
2. 添加自定义域名（如 quicktool.xin）
3. 修改域名 DNS 设置：
   - 添加 CNAME 记录：`www.quicktool.xin` → `cname.vercel-dns.com`
   - 或添加 A 记录（根域名）
4. 等待 DNS 生效（通常几分钟到几小时）

---

## 三、Netlify 部署步骤

### 3.1 拖拽部署

1. 访问 https://app.netlify.com/drop
2. 将项目文件夹拖拽到上传区域
3. 等待部署完成
4. 获取随机生成的子域名（如 quicktool-xxx.netlify.app）

### 3.2 Git 集成部署

1. 将项目推送到 GitHub
2. 在 Netlify 控制台点击 "New site from Git"
3. 选择 GitHub 仓库
4. 点击 "Deploy site"

### 3.3 自定义域名

1. 在 Netlify 控制台选择项目 → Domain settings
2. 添加自定义域名
3. 配置 DNS（与 Vercel 类似）
4. Netlify 会自动配置 SSL 证书

---

## 四、GitHub Pages 部署步骤

### 4.1 仓库准备

1. 创建 GitHub 仓库（建议命名：`quicktool-xin`）
2. 将项目代码推送到 `main` 分支
3. 仓库设置 → Pages → Source 选择 main 分支

### 4.2 访问地址

- 默认地址：`https://username.github.io/quicktool-xin/`
- 自定义域名：在仓库根目录创建 `CNAME` 文件，内容为 `www.quicktool.xin`

### 4.3 GitHub Actions 自动部署

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

---

## 五、部署后检查清单

### 5.1 功能检查

- [ ] 首页正常加载
- [ ] 所有25个工具页面可访问
- [ ] 深浅主题切换正常
- [ ] 导航菜单正常工作
- [ ] 广告位正常显示（启用后）
- [ ] Service Worker 正常注册
- [ ] Analytics 正常记录

### 5.2 SEO 检查

- [ ] Google Search Console 提交 sitemap
- [ ] Bing Webmaster Tools 提交 sitemap
- [ ] robots.txt 可访问
- [ ] sitemap.xml 可访问
- [ ] 所有页面有正确的 title 和 meta description

### 5.3 性能检查

- [ ] PageSpeed Insights 得分 > 80
- [ ] Lighthouse 性能评分
- [ ] 移动端适配检查

### 5.4 广告检查（启用后）

- [ ] AdSense 代码正确加载
- [ ] 广告位显示正常
- [ ] 无布局偏移问题

---

## 六、域名配置

### 6.1 DNS 记录配置

以腾讯云 DNS 为例：

```
类型    主机记录    记录值                    TTL
-----------------------------------------------------
CNAME  www        cname.vercel-dns.com      600
A      @          76.76.21.21               600
```

### 6.2 SSL 证书

- Vercel/Netlify 自动配置 HTTPS
- GitHub Pages 需要手动配置或等待自动签发
- 腾讯云 COS 需要购买或申请免费证书

---

## 七、常见问题

### Q1: 部署后 404 错误？
- 检查发布目录是否正确
- 检查路由配置（SPA 需要特殊配置）

### Q2: Service Worker 不工作？
- 确保通过 HTTPS 访问
- 检查 sw.js 文件路径

### Q3: 广告不显示？
- 确认 AdSense 已审核通过
- 检查 AD_CONFIG.enabled 是否为 true
- 等待几小时让广告正常展示

### Q4: 自定义域名不生效？
- 等待 DNS 生效（最长48小时）
- 检查 DNS 记录是否正确
- 清除浏览器缓存

---

## 八、监控与维护

### 8.1 网站监控

- **Uptime Robot**: 免费监控网站可用性
- **Google Search Console**: 监控 SEO 表现
- **Google Analytics**: 监控流量和用户行为

### 8.2 定期维护

- 每月检查工具功能是否正常
- 每季度更新一次营销内容
- 根据用户反馈持续优化工具

---

## 九、备份方案

### 9.1 代码备份
- GitHub 仓库自动备份
- 定期本地备份

### 9.2 数据备份
- 网站数据均在客户端，无需服务端备份
- 配置文件（analytics.js、common.js）建议版本控制

---

**部署完成后，进入流量获取和变现阶段！**
