# الانحدار اللوجستي (Logistic Regression)الهدف: التصنيف الثنائي أو المتعدد (Binary/Multiclass Classification) مثل تصنيف بريد إلكتروني (مزعج / غير مزعج).
# الشرح الرياضي:النموذج يأخذ مخرجات المعادلة الخطية ويحشرها داخل دالة السيروميد (Sigmoid) 
لإنتاج احتمالية محصورة بين 0 و 1:
* \(\^{y}=\sigma (XW+b)=\frac{1}{1+e^{-(XW+b)}}\)

# دالة الخسارة (Binary Cross-Entropy / Log Loss):
* \(J(W,b)=-\frac{1}{n}\sum _{i=1}^{n}\left[y_{i}\log (\^{y}_{i})+(1-y_{i})\log (1-\^{y}_{i})\right]\)
