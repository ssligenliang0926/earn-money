/* =========================================================
 * 极简工具箱 · 高搜索量工具开发指南
 * 基于搜索量和商业价值的新工具建议
 * ========================================================= */

/**
 * 新增工具优先级排序（基于搜索量和商业价值）
 * 
 * 优先级计算公式: 搜索量 × 商业价值系数 × 竞争难度倒数
 */

const HIGH_PRIORITY_TOOLS = [
  {
    name: 'JSON 转 CSV',
    file: 'json-to-csv.html',
    icon: '📊',
    searchVolume: '高',
    commercialValue: '高',
    competition: '中',
    priority: 95,
    desc: 'JSON 数据一键转换为 CSV 格式，支持嵌套 JSON 展开',
    seo: {
      title: 'JSON 转 CSV - 在线 JSON 数据转换工具 | 极简工具箱',
      description: '免费在线 JSON 转 CSV 工具，支持嵌套 JSON 展开、自定义分隔符、UTF-8 编码。无需注册，打开即用。',
      keywords: 'JSON转CSV,JSON转Excel,JSON导出CSV,CSV转换,数据转换'
    },
    implementTime: '2-3小时',
    features: [
      '粘贴 JSON 数据，一键转换为 CSV',
      '支持嵌套 JSON 自动展开',
      '自定义字段选择和列顺序',
      '支持 UTF-8 BOM（Excel 兼容）',
      '下载 CSV 文件或复制内容'
    ]
  },
  {
    name: 'Excel 转 JSON',
    file: 'excel-to-json.html',
    icon: '📋',
    searchVolume: '高',
    commercialValue: '高',
    competition: '中',
    priority: 92,
    desc: 'Excel/CSV 数据转换为 JSON 格式，支持多行表头',
    seo: {
      title: 'Excel 转 JSON - 在线数据转换工具 | 极简工具箱',
      description: '免费在线 Excel 转 JSON 工具，支持 CSV 上传和粘贴，自动生成 JSON 数组。纯前端处理，数据不上传服务器。',
      keywords: 'Excel转JSON,CSV转JSON,表格转JSON,数据转换'
    },
    implementTime: '2-3小时',
    features: [
      '支持 Excel/CSV 文件上传',
      '支持粘贴表格数据',
      '自动生成 JSON 数组',
      '自定义字段名映射',
      '支持多行表头'
    ]
  },
  {
    name: 'JWT 解码器',
    file: 'jwt-decoder.html',
    icon: '🔐',
    searchVolume: '高',
    commercialValue: '中',
    competition: '高',
    priority: 88,
    desc: '在线 JWT Token 解码和验证，查看 Header/Payload',
    seo: {
      title: 'JWT 解码器 - 在线 JWT Token 解析工具 | 极简工具箱',
      description: '免费在线 JWT 解码器，支持解码 JWT Token，查看 Header 和 Payload，验证 Token 签名。纯前端实现，Token 不上传服务器。',
      keywords: 'JWT解码,JWT解析,Token解码,JWT验证,JSON Web Token'
    },
    implementTime: '1-2小时',
    features: [
      '粘贴 JWT Token，自动解码',
      '显示 Header 和 Payload',
      'Base64 自动解码',
      'Token 过期时间显示',
      '纯前端解码，安全保密'
    ]
  },
  {
    name: '图片转 Base64',
    file: 'image-to-base64.html',
    icon: '🖼️',
    searchVolume: '中',
    commercialValue: '中',
    competition: '高',
    priority: 80,
    desc: '图片转换为 Base64 编码，支持多种输出格式',
    seo: {
      title: '图片转 Base64 - 在线图片编码工具 | 极简工具箱',
      description: '免费在线图片转 Base64 工具，支持 PNG/JPEG/WebP，输出 Data URL、纯 Base64、CSS/HTML 格式。本地处理，图片不上传。',
      keywords: '图片转Base64,图片编码,Base64编码,Data URL'
    },
    implementTime: '1-2小时',
    features: [
      '上传图片自动转换',
      '支持 PNG/JPEG/WebP',
      '多种输出格式（Data URL/纯Base64/CSS/HTML）',
      '图片大小限制提示',
      '本地处理，隐私安全'
    ]
  },
  {
    name: 'Markdown 转 HTML',
    file: 'markdown-to-html-converter.html',
    icon: '📝',
    searchVolume: '中',
    commercialValue: '中',
    competition: '高',
    priority: 78,
    desc: 'Markdown 实时转换为 HTML，支持导出和预览',
    seo: {
      title: 'Markdown 转 HTML - 在线转换工具 | 极简工具箱',
      description: '免费在线 Markdown 转 HTML 工具，实时预览，支持代码高亮、表格、数学公式。纯前端渲染，Markdown 不上传服务器。',
      keywords: 'Markdown转HTML,Markdown转换,在线编辑器,MD转HTML'
    },
    implementTime: '2-3小时',
    features: [
      '实时预览 Markdown',
      '支持 GFM 语法（表格、任务列表）',
      '代码高亮',
      '导出 HTML 文件',
      '全屏编辑模式'
    ]
  },
  {
    name: 'Lorem Ipsum 生成器',
    file: 'lorem-ipsum-generator.html',
    icon: '📄',
    searchVolume: '中',
    commercialValue: '低',
    competition: '中',
    priority: 65,
    desc: '生成 Lorem Ipsum 占位文本，支持段落/列表/单词数',
    seo: {
      title: 'Lorem Ipsum 生成器 - 占位文本生成工具 | 极简工具箱',
      description: '免费在线 Lorem Ipsum 生成器，支持自定义段落数、句子数、单词数。设计师和开发者的排版必备工具。',
      keywords: 'Lorem Ipsum,占位文本,填充文本,设计素材'
    },
    implementTime: '1小时',
    features: [
      '自定义段落/句子/单词数量',
      '多种语言支持（拉丁文/英文/中文）',
      '一键复制',
      '随机生成选项'
    ]
  },
  {
    name: 'Unix 时间戳转换器',
    file: 'unix-timestamp.html',
    icon: '⏰',
    searchVolume: '高',
    commercialValue: '低',
    competition: '中',
    priority: 85,
    desc: 'Unix 时间戳与日期时间互转，支持秒/毫秒',
    seo: {
      title: 'Unix 时间戳转换 - 在线时间戳工具 | 极简工具箱',
      description: '免费在线 Unix 时间戳转换工具，支持秒/毫秒自动识别，实时显示当前时间戳，支持多时区转换。',
      keywords: 'Unix时间戳,时间戳转换,时间戳转日期,日期转时间戳'
    },
    implementTime: '1-2小时',
    features: [
      '秒/毫秒自动识别',
      '实时显示当前时间戳',
      '多时区支持',
      '一键复制结果'
    ]
  },
  {
    name: '颜色对比度检测',
    file: 'color-contrast-checker.html',
    icon: '🎨',
    searchVolume: '中',
    commercialValue: '中',
    competition: '低',
    priority: 75,
    desc: '检测前景色和背景色的对比度，符合 WCAG 标准',
    seo: {
      title: '颜色对比度检测 - WCAG 无障碍配色工具 | 极简工具箱',
      description: '免费在线颜色对比度检测工具，符合 WCAG 2.1 标准，帮助设计师创建无障碍配色方案。支持 AA/AAA 等级判定。',
      keywords: '颜色对比度,WCAG,无障碍设计,配色检测,对比度检测'
    },
    implementTime: '2-3小时',
    features: [
      '实时预览颜色效果',
      '自动计算对比度比率',
      'WCAG AA/AAA 等级判定',
      '色盲模拟预览',
      '一键复制配色代码'
    ]
  }
];

// 导出推荐
module.exports = {
  HIGH_PRIORITY_TOOLS,
  RECOMMENDED_FIRST: ['JWT 解码器', 'JSON 转 CSV', 'Excel 转 JSON', 'Unix 时间戳转换器']
};
