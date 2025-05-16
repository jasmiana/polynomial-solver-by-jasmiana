from setuptools import setup, find_packages

setup(
    name='polynomial-solver',       # 软件包名称，支持自定义
    version='0.1.1',                # 版本号，根据需要修改
    packages=find_packages(),       # 自动查找包含 __init__.py 的目录作为包
    install_requires=[
        # 如果您的项目依赖于任何第三方库，请在此列出
        # 例如： 'sympy',
    ],
    entry_points={
        # 如果您希望安装后可以通过命令行运行某个函数，可以在这里配置
        # 例如，如果您想让 main.py 中的 solve_expression 函数可以通过命令行调用：
        # 'console_scripts': [
        #     'poly-solve=main:solve_expression',
        # ],
    },
    author='jasmiana', # 作者名称
    author_email='lune07525@gmail.com', # 作者邮箱
    description='A Python-based tool for simplifying polynomials and fractional polynomials', # 项目描述
    long_description=open('README.md', encoding='utf-8').read(), # 使用 README.md 作为详细描述
    long_description_content_type='text/markdown', # 详细描述的格式
    url='https://github.com/jasmiana/polynomial-solver-by-jasmiana', # 项目的 URL (例如 GitHub 仓库)
    classifiers=[
    # 开发状态 (Development Status)
    # 选择一个描述项目当前状态的分类器
    # 1 - Planning (计划中)
    # 2 - Pre-Alpha (早期 Alpha)
    # 3 - Alpha (Alpha 版本)
    # 4 - Beta (Beta 版本)
    # 5 - Production/Stable (生产/稳定版)
    # 6 - Mature (成熟)
    # 7 - Inactive (不活跃)
    'Development Status :: 4 - Beta', # 假设项目处于 Beta 测试阶段

    # 目标受众 (Intended Audience)
    # 谁会使用这个软件包
    'Intended Audience :: Developers',        # 开发者
    'Intended Audience :: Education',          # 教育者/学生
    'Intended Audience :: Science/Research',   # 科学家/研究人员

    # 许可证 (License)
    # 项目使用的许可证，通常与 setup() 中的 license 参数一致
    'License :: OSI Approved :: MIT License', # 根据您的 setup.py，这是 MIT 许可证

    # 编程语言 (Programming Language)
    # 项目使用的编程语言和版本
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6', # 根据 python_requires='>=3.6'
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12', # 添加您支持的所有 Python 3 版本

    # 操作系统兼容性 (Operating System)
    # 项目兼容的操作系统
    'Operating System :: OS Independent', # 如果项目不依赖特定操作系统，使用这个

    # 主题 (Topic)
    # 项目的主要主题或应用领域
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6', # 指定项目所需的 Python 版本
)