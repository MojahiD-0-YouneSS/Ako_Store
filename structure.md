ShopTools --> data analysition and visualisation
cart --> stros order and shoping history
client -->  client data
coordinations --> tarack orders
order --> validated purshesed product
receipt --> proof of purshse
reviews --> ofred by client
shopingHistory --> all orders orders ordered by time
storeApi --> Api
translator --> translates the text into 4 languages
Shop -->  owner view of the chope to post pruducted get orders and manage receipts
adminProfile --> manipulate / edit the items
checkout --> validatet by cilent
conversation --> client to shop
core -->  ony thing that not related to shop or client
headline -->  products with headline cheked
product --> responsible for products listing and see details
search --> search functionallity

apps to add:

Online Payment
InventoryManagement
PromotionsCoupons
ShippingLogistics
UserAuthenticationAuthorization
AnalyticsReporting
SocialMediaIntegration
InternationalizationLocalization
CustomerSupport
EmailMarketing
ReturnsRefunds
ProductRecommendations
Security
SEOOptimization
PerformanceOptimization
ContentManagement
FeedbackSurveys" V

apps relation ship:
*******************

ShopTools.RelatioshipWith(all(data related))
cart.RelatioshipWith(order)
client.RelatioshipWith()
coordinations.RelatioshipWith()
order.RelatioshipWith(product, client)
receipt.RelatioshipWith(order, client, shop)
reviews.RelatioshipWith(client , product)
shopingHistory.RelatioshipWith(order)
storeApi.RelatioshipWith()
translator.RelatioshipWith(templates)
Shop.RelatioshipWith(product, client, order, receipt, cart)
adminProfile.RelatioshipWith(all)
checkout.RelatioshipWith(client, product, shop)
conversation.RelatioshipWith(client, shop)
core.RelatioshipWith()
headline.RelatioshipWith(products, templates='core')
product.RelatioshipWith(shop, client)
search.RelatioshipWith(products)


