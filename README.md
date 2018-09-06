# image_clipper 在线图片裁剪

## 功能需求：    
假设某个markdown的blog平台, 用户会在markdown中使用很多第三方的图片链接, 然后在展示图片的时候, 我们需要实时地拉取第三方的图片(场景只是假设, 可能不是最好的方案), 然后又因为图片在Blog中的不同场景以及不同平台, 为了图片的流量优化, 我们需要使用不同大小的图片, 所以我们需要写一个图片的在线剪裁代理服务, 功能描述如下:

假设你的服务会部署在域名 `image.transform.online`, 那用户可以通过 `http://image.transform.online/{transform_params}/{image_url}` 的这种URL获取到经过处理的`{image_url}`的版本，参数说明如下：

> `{image_url}` 是一个图片的url, 比如 `https://imgsa.baidu.com/forum/pic/item/462309f790529822a8f35517dbca7bcb0b46d426.jpg`    

> `{transform_params}` 是一个由因为逗号(,)分割的字符串, 每个字符串都是一个转换的参数, 目前支持转换参数如下:    

  > `w_{width_in_pixel}`: 等比缩放图片到高度为width_in_pixel像素    
  > `h_{height_in_pixel}`: 等比缩放图片到高度为height_in_pixel像素    
  > 如果只有h参数的情况, 就把图片压缩到对应的高度, 如果只有w就压缩到对应的宽度, 如果h和w都有的情况下, 就按照保证图片全部展示并满足其中一个高和宽的参数处理.


## 服务方案设计
根据需求说明，本服务的主要功能为：对图片链接所对应的图片，根据用户指定的高度和宽度，进行等比的缩放，返回给用户一个处理后的图片。        
功能的实现分为两部分，对请求的url请求体`http://image.transform.online/{transform_params}/{image_url}`进行解析后得到图片的url链接及size参数：    
    第一部分为图片链接的获取，这里使用第三方包`requests`对解析图片链接，获取链接的headers信息，判断链接是否为图片链接，如果是图片的话，下载原始图片，否则返回异常信息；     
    第二部分为图片的裁剪处理，这里使用第三方包`pillow`对图片进行处理，根据用户的参数要求对图片进行裁剪缩放处理；    
    本次web服务的框架采用Django框架，对此功能进行了封装处理，并增加操作日志记录。    


## 项目中遇到的问题及解决方法：
项目中主要遇到了以下这个问题：    

对用户url请求体的获取。因为图片url链接经常会带有query参数，类似`https://timgsa.baidu.com/timg/?image&quality=80&size=b9999_10000&sec=1536229123287&di=696e08f26ecf418cdc3766f321c00d28&imgtype=0&src=http%3A%2F%2Fh.hiphotos.baidu.com%2Fzhidao%2Fwh%253D450%252C600%2Fsign%3D86ccfde9d01373f0f56a679b913f67cd%2Fd009b3de9c82d1589b303c23810a19d8bd3e42f5.jpg`，我在路由配置的时候本想直接在url中获取我所需的参数和图片url链接，但是url中`?`后面的内容都会被当作query参数处理，因此我修改了路由匹配的参数，不再在路由过滤的时候取得图片参数和url链接，改为在接口中直接获取整串用户传递过来的url请求体进行后续处理
