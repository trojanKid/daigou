export class Product {
  style_id; // style//:款号
  product_name;  // 商品名
  details_url;  // 商品详细信息页的url
  list_price;  // 原价
  sale_price;  // 折后价（不含税）
  is_limited_sale;  // 是否是限时折扣,True是False否
  show_img;  // 展示图对应的url
  available_colors;  // 本商品所含的颜色
  is_available_now;  // 是否当前是可买的
  design_description;  //设计描述
  details;  //详细参数
  sale_message; // 关于本次折扣的描述
  sale_deadline;  //  折扣结束日期
  rate_value;  // 评分
  review_count;  // 评论数
  materials;  // 材质
  size;  // 尺寸
}
