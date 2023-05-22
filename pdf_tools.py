import datetime
import time

from PIL import Image
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

# import fitz

"""
合成文件夹下的所有图片为pdf
    Args:
    img_folder_path (str): 源文件夹

"""


def combine_imgs(img_folder_path):
    # 列出给定目录中的所有文件和目录，并构建图像文件列表
    files = os.listdir(img_folder_path)

    png_files = []
    for file in files:
        if 'png' in file or 'jpeg' in file:
            png_files.append(img_folder_path + file)

    total_pages = len(png_files)
    # 若png_files数组为空，则跳出函数
    if total_pages == 0:
        print(f"No imgs files found in {img_folder_path}")
        return
    # 对图像文件列表进行排序以确保它们按先后顺序被添加到PDF中
    png_files.sort()

    """
    通过 output 对象保存第一张 PNG 图片，并将其作为输出 PDF 文件的第一页。然后该脚本遍历 png_files 列表中的剩余 PNG 图片，
    将它们作为 append_images 参数添加到输出 PDF 文件中。
    因此，为了防止第一张 PNG 绘制两次，需要先从 png_files 中删除第一张 PNG 图像。这是通过 png_files.pop(0) 代码实现的
    """
    output = Image.open(png_files[0])
    png_files.pop(0)
    # 将剩余的PNG文件打开并转换为RGB模式
    sources = []
    for file in png_files:
        png_file = Image.open(file)
        # 如果PNG图像是RGB类型，则不需要转换
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)
    current_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    out_file_path = img_folder_path + 'img'+current_time+'.pdf'
    # 将输出图像另存为PDF文件并添加其余PNG图像作为附加图像
    output.save(out_file_path, "pdf", save_all=True, append_images=sources)
    print('执行成功，已将' + str(total_pages) + '页图片合并为PDF文件')


"""
    合成文件夹下的所有pdf为pdf
    Args:
    folder_path (str): 源文件夹
    pdf_file_path (str): 输出路径
"""

def combine_pdfs(pdf_folder_path):
    # 打开该文件夹中的所有 PDF 文件并将它们合并成一个输出 PDF 文件。
    # merger = PyPDF2.PdfFileMerger()
    merger = PdfMerger()
    pdf_files = []
    for file_name in os.listdir(pdf_folder_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(pdf_folder_path, file_name)
            input_pdf = PdfReader(open(file_path, 'rb'))
            pdf_files.append(input_pdf)
    if len(pdf_files) == 0:
        print(f"No PDF files found in {folder_path}")
        return
    elif len(pdf_files) == 1:
        print(f"Only one PDF file found in {folder_path}. can not merge.")
        return

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    current_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    out_file_path = pdf_folder_path + 'combine'+current_time+'.pdf'
    with open(out_file_path, 'wb') as f:
        merger.write(f)
    print('执行成功，已将'+ str(len(pdf_files)) +'个PDF文件合并为新的PDF文件')

# PDF压缩，但压缩效果一般
def compress_pdf(compress_folder_path):
    # 打开输入 PDF 文件并创建一个新的 PDF 文件写入器
    files = os.listdir(compress_folder_path)
    compress_files = []
    for file in files:
        if '.pdf' in file:
            compress_files.append(compress_folder_path + file)
    if len(compress_files) == 0:
        print(f"No pdf files found in {compress_folder_path}.请放入需要压缩的PDF文件")
        return
    if len(compress_files) > 1: # 该文件夹内多于一个文件则退出执行，也可写成多于一个文件进行循环操作
        print(f"More than one PDF files found in {compress_folder_path}. can not compress.")
        return

    print(compress_files[0])
    input_pdf = PdfReader(open(compress_files[0], "rb"))
    output_pdf = PdfWriter()

    # 遍历输入文档的每一页，并将它们添加到输出 PDF 文件中
    for page in range(len(input_pdf.pages)):
        current_page = input_pdf.pages[page]
        current_page.compress_content_streams()
        output_pdf.add_page(current_page)
    current_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    out_file_path = compress_folder_path + 'compress' + current_time + '.pdf'
    # 将输出 PDF 写入到目标文件中
    with open(out_file_path, "wb") as f:
        output_pdf.write(f)
    print('执行成功，已成功压缩PDF文件')

if __name__ == "__main__":
    folder = r"/Users/j/Desktop/pdf_tool/"

    # 为每个可用的功能指定名称和相应的函数对象
    functions = {
        "compress": compress_pdf, # 选择压缩pdf文件
        "combine_imgs": combine_imgs, # 选择合并图片为pdf
        "combine_pdfs": combine_pdfs # 选择合并多个PDF文件
    }
    # 根据需要运行的函数名称从映射字典中获取函数对象
    function_name = "compress"  # 可以更改该名称以选择不同函数
    selected_function = functions.get(function_name)

    # 如果没有找到匹配的函数，则打印错误消息并退出程序
    if not selected_function:
        print(f"No function found with name: {function_name}")
        exit()
    # 将参数传递给所选的函数并运行它
    if function_name == "compress":
        folder_path = folder + "compress/"
        selected_function(folder_path)
    elif function_name == "combine_imgs":
        folder_path = folder + 'img/'
        selected_function(folder_path)
    elif function_name == "combine_pdfs":
        folder_path = folder + 'pdf/'
        selected_function(folder_path)
