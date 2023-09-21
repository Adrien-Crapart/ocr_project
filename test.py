
# image_to_ocr = cv2.imread("pdf_test.jpg")
# # Convert to Gray
# preprocessed_img = cv2.cvtColor(image_to_ocr, cv2.COLOR_BGR2GRAY())
# # Do Binary and Otsu Thresholding
# preprocessed_img = cv2.threshold(
#     preprocessed_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# # Median Blur to remove noise in the image
# preprocessed_img = cv2.medianBlur(preprocessed_img, 3)

# cv2.imwrite("temp_img.jpg", preprocessed_img)
# preprocessed_pil_img = Image.open("temp_img.jpg")

# text_extracted = pytesseract.image_to_string(Image.open("temp_img.jpg"))
# cv2.imshow('Video', image_to_ocr)
