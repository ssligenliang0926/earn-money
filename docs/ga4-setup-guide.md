# 极简工具箱 - GA4 配置指南

## 一、创建 GA4 属性

### 1.1 注册 Google Analytics

1. 访问 https://analytics.google.com
2. 点击"开始测量"
3. 输入账户名称（如"极简工具箱"）
4. 选择报告地域时区
5. 输入财产名称（如"quicktool.xin"）
6. 选择行业类别
7. 选择业务规模

### 1.2 获取 Measurement ID

1. 完成设置向导
2. 选择"网页"作为平台
3. 输入网址：https://quicktool.xin/
4. 点击"创建流"
5. 复制 Measurement ID（格式：G-XXXXXXXXXX）

---

## 二、配置 analytics.js

### 2.1 修改配置

打开 `E:\earn_money\js\analytics.js`，修改以下配置：

```javascript
window.ANALYTICS_CONFIG = {
  ga4: {
    enabled: true,
    trackingId: 'G-XXXXXXXXXX'  // 替换为你的 GA4 Measurement ID
  },
  baidu: {
    enabled: false,
    token: ''
  }
};
```

### 2.2 部署更新

1. 保存文件
2. 重新部署网站
3. 访问网站，确认 GA4 正常记录

---

## 三、验证安装

### 3.1 实时验证

1. 打开 GA4 后台 → 实时报告
2. 访问你的网站
3. 确认看到活跃用户

### 3.2 调试工具

使用 Chrome 扩展 "GA Debugger" 或浏览器控制台：

```javascript
// 在控制台运行
console.log('GA4 配置:', window.ANALYTICS_CONFIG);
```

---

## 四、关键指标设置

### 4.1 自定义事件追踪

analytics.js 已自动追踪以下事件：

| 事件 | 触发时机 | 参数 |
|------|----------|------|
| page_view | 页面加载 | path, title |
| tool_open | 打开工具页 | tool_name |

### 4.2 自定义指标

建议在 GA4 后台设置以下指标：

1. **工具使用率**
   - 事件：tool_open
   - 参数：tool_name

2. **广告点击率**
   - 事件：ad_click（待实现）

3. **页面停留时长**
   - 自动收集

### 4.3 自定义报告

创建以下报告：

1. **工具使用报告**
   - 维度：工具名称
   - 指标：事件次数、活跃用户

2. **流量来源报告**
   - 维度：默认渠道分组
   - 指标：用户数、会话数

3. **用户行为报告**
   - 维度：页面路径
   - 指标：浏览数、平均停留时间

---

## 五、百度统计配置（可选）

如果需要同时使用百度统计：

### 5.1 获取 Token

1. 访问 https://tongji.baidu.com
2. 添加网站
3. 复制代码中的 token

### 5.2 修改配置

```javascript
window.ANALYTICS_CONFIG = {
  ga4: { enabled: false, trackingId: '' },
  baidu: {
    enabled: true,
    token: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  }
};
```

---

## 六、常见问题

### Q1: GA4 没有数据？
- 检查 trackingId 是否正确
- 等待 24-48 小时（GA4 数据延迟）
- 清除浏览器缓存重试

### Q2: 事件没有触发？
- 检查浏览器控制台是否有错误
- 确认 analytics.js 已正确加载
- 检查 GA4 后台的事件配置

### Q3: 实时报告没有数据？
- 确认 Analytics Config 中 enabled 为 true
- 确认 Tracking ID 正确
- 刷新页面后查看实时报告

---

## 七、隐私合规

### 7.1 GDPR 提示

如需面向欧洲用户，需要：
1. 添加 Cookie 同意横幅
2. 提供隐私政策页面
3. 确保数据处理合规

### 7.2 隐私政策

建议在网站添加隐私政策页面，说明：
- 使用 GA4 进行数据分析
- 不收集个人身份信息
- 数据仅用于网站优化

---

**配置完成后，开始在 GA4 后台监控网站数据！**
