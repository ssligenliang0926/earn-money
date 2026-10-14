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

1. 创建 GitHub 仓库（本项目实际使用：`ssligenliang0926/earn-money`）
2. 将项目代码推送到 `main` 分支
3. 仓库设置 → Pages → Source 选择 `main` 分支，目录选 `/` (root)

### 4.2 访问地址

- 默认地址：`https://ssligenliang0926.github.io/earn-money/`
- 自定义域名：在仓库根目录创建 `CNAME` 文件，**内容为 `quicktool.xin`（apex 裸域，不要写 `www.`）**

> ⚠️ **重要：CNAME 文件内容必须是 apex 裸域 `quicktool.xin`。**
> 若误写为 `www.quicktool.xin`，GitHub Pages 会把站点绑定到 www 子域，
> 而 DNS 的 A 记录指向 apex，两者不匹配会导致全站 404。
>
> 该文件曾在提交 `9b87b77` 中被误删，导致 `quicktool.xin` 返回
> "There isn't a GitHub Pages site here."，已于 `61b4232` 恢复。
> 修改首页或 SEO 时请勿顺带删除此文件。

### 4.3 www 子域重定向（GitHub Pages 自动处理）

GitHub Pages 会在 apex 与 www 之间自动重定向，**无需在代码或 DNS 中额外配置**，
只需同时满足：

1. 仓库 `CNAME` 文件内容为 apex 裸域：`quicktool.xin`
2. DNS 中存在 www 的 CNAME 记录：`www.quicktool.xin` → `ssligenliang0926.github.io`
   （注意：指向 `<user>.github.io`，**不含仓库名**）

配置正确后，`https://www.quicktool.xin/任意路径` 会 301 跳转到 `https://quicktool.xin/对应路径`。

> 注意：DNS 的 `CNAME` **记录**（用于域名解析）与仓库里的 `CNAME` **文件**
> （用于 GitHub Pages 认领域名）是两个不同的东西，不要混淆。

### 4.4 GitHub Actions 自动部署（可选）

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
- [ ] 所有28个工具页面可访问
- [ ] `CNAME` 文件存在且内容为 `quicktool.xin`（apex，不含 www）
- [ ] `https://quicktool.xin/` 返回 200
- [ ] `https://www.quicktool.xin/` 301 跳转到 apex
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

### 6.1 DNS 记录配置（本项目实际使用：GitHub Pages）

以下是 `quicktool.xin` **当前生效**的 DNS 配置（已实测验证）：

```
类型    主机记录    记录值                        TTL
---------------------------------------------------------
A      @          185.199.108.153               600
A      @          185.199.109.153               600
A      @          185.199.110.153               600
A      @          185.199.111.153               600
CNAME  www        ssligenliang0926.github.io    600
```

要点：

- apex（`@`）使用 GitHub Pages 官方的 4 个 A 记录，四个都要加
- `www` 的 CNAME 指向 `<user>.github.io`，**不要带仓库名**
- 如需 IPv6，可另加 `AAAA` 记录：`2606:50c0:8000::153` ~ `2606:50c0:8003::153`
- 切勿使用泛解析 `*.quicktool.xin`，会带来域名被他人接管的
  风险（参见 GitHub 官方文档的安全警告）

> 若改用 Vercel 部署，DNS 需改为 `cname.vercel-dns.com` 与 `76.76.21.21`；
> 切换平台时务必同步修改，否则会出现域名解析到 A 平台、
> 站点却部署在 B 平台的 404 情况。

### 6.2 SSL 证书

- GitHub Pages 在绑定自定义域名后**自动签发** Let's Encrypt 证书
  （实测：`CN=quicktool.xin`，SAN 同时覆盖 `quicktool.xin` 与 `www.quicktool.xin`）
- 证书签发通常在 DNS 生效后几分钟到 24 小时内完成
- 签发完成后，建议在 Settings → Pages 勾选 **Enforce HTTPS**
- Vercel / Netlify 同样自动配置 HTTPS
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

### Q5: 访问域名显示 "There isn't a GitHub Pages site here."？

这是 **GitHub Pages 找不到域名归属**，不是网站宕机。按顺序排查：

1. **检查仓库根目录是否有 `CNAME` 文件**，内容必须是 apex 裸域：

   ```
   quicktool.xin
   ```

   这是最常见的原因——该文件被误删后，DNS 依然正常解析到 GitHub，
   但 GitHub 收到请求后不知道返回哪个仓库，于是返回此 404 页面。
   查看是否为误删：`git log --oneline -- CNAME`

2. 确认 `CNAME` 内容**不含 `www.`**（写错会导致全站 404）

3. 用 GitHub API 确认平台侧已认领域名（`cname` 字段不应为 `null`）：

   ```bash
   gh api repos/ssligenliang0926/earn-money/pages
   ```

4. 确认 DNS 的 A 记录指向 GitHub Pages 官方 IP（见 6.1 节）

> 注意：只有**根路径**返回该 404、而其他路径能正常 301 时，
> 通常是 GitHub 边缘节点上的**旧缓存尚未过期**（响应头
> `X-Cache: HIT`、`Age` 较大），等待其过期即可，无需改动代码。

### Q6: apex 与 www 之间的重定向如何生效？

由 GitHub Pages **自动处理**，无需写代码或重定向规则，只需：

- 仓库 `CNAME` 文件内容为 apex 裸域 `quicktool.xin`
- DNS 存在 `www` → `ssligenliang0926.github.io` 的 CNAME 记录

两者齐备后，`www` 会自动 301 到 apex（反之亦然，取决于 `CNAME` 里配置的是哪个）。

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
