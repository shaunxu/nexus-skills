---
title: "托管数据生命周期"
lastUpdated: 2026-07-03T07:06:20.000Z
---

# 托管数据生命周期

本文档详细阐述在 Nexus 平台存储托管数据的生命周期，不包括远程或其他方式的数据存储。

## 数据与应用生命周期

应用生命周期的每个阶段，都会影响管理和存储数据的方式，以下是详细介绍。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.55%" /><col style="width: 73.45%" /></colgroup><thead><tr><th>阶段</th><th>描述</th></tr></thead><tbody><tr><td>创建/部署</td><td>当开发者创建或部署应用时，这些阶段不会设置任何存储空间，系统会定义应用并使其可供使用，但在将应用其安装到企业之前，不会创建或存储任何数据</td></tr><tr><td>安装</td><td>当应用被安装到某个企业时，会在平台中配置存储空间，用于管理该特定企业的应用数据</td></tr><tr><td>升级</td><td>当应用升级新版本时，如果新功能需要存储空间，系统会在应用升级期间额外配置存储，以满足新的存储需求，同时不影响现有企业数据</td></tr><tr><td>卸载</td><td>当应用被卸载时，数据会被「软删除」，在保留期内保存 <code>30天</code></td></tr><tr><td>删除</td><td>如果要删除应用，必须先卸载当前应用所有安装实例，随后系统将按照上述相同的卸载保留期来管理数据</td></tr></tbody></table>

## 数据保留与删除策略

数据保留或删除方式取决于应用的状态。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.54%" /><col style="width: 72.46%" /></colgroup><thead><tr><th>阶段</th><th>描述</th></tr></thead><tbody><tr><td>重新安装</td><td>如果应用被重新安装，则视为全新安装。但是如果在卸载后的 <code>30天</code> 内提出请求，新安装可以与旧数据重新关联</td></tr><tr><td>保留期结束</td><td>在 <code>30天</code> 保留期结束后，所有托管数据将会被彻底删除，且无法恢复</td></tr></tbody></table>
