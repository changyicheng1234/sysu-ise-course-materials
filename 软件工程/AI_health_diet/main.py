from flask import Flask, render_template, request, jsonify, session
from diet_agent import (
    create_diet_agent,
    generate_diet_recommendation,
    analyze_meals,
    generate_recipe,
    generate_takeout_recommendation,
    generate_economical_diet,  
    SMART_DIET_ROLE,
    DIET_ANALYZE_ROLE,
    DIET_RECIPE_GENERATOR_ROLE,
    TAKEOUT_RECOMMENDATION_ROLE,
    ECONOMICAL_ROLE  
)
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        data = request.get_json()
        agent = create_diet_agent(SMART_DIET_ROLE)
        
        # 获取用户配置信息
        user_profile = session.get('user_profile', {})
        health_stats = session.get('health_stats', {})
        
        # 组合推荐所需的所有信息
        recommendation_data = {
            'health_goal': data.get('health_goal', user_profile.get('health_goal')),
            'dietary_preferences': data.get('dietary_preferences', ''),
            'lifestyle': data.get('lifestyle', ''),
            'daily_calories': health_stats.get('daily_calories', 2000),
            'daily_nutrition': health_stats.get('daily_nutrition', {}),
            'bmi': health_stats.get('bmi'),
            'gender': user_profile.get('gender'),
            'age': user_profile.get('age')
        }
        
        # 调用推荐函数并直接返回结果
        result = generate_diet_recommendation(agent, **recommendation_data)
        return jsonify(result)
        
    return render_template('recommend.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        try:
            data = request.get_json()
            agent = create_diet_agent(DIET_ANALYZE_ROLE)
            result = analyze_meals(agent, data['meals'])
            
            # 确保结果格式正确
            formatted_result = {
                '早餐分析': '',
                '午餐分析': '',
                '晚餐分析': '',
                '营养建议': ''
            }
            
            if isinstance(result, dict):
                formatted_result.update({
                    '早餐分析': result.get('早餐分析', '暂无分析数据'),
                    '午餐分析': result.get('午餐分析', '暂无分析数据'),
                    '晚餐分析': result.get('晚餐分析', '暂无分析数据'),
                    '营养建议': result.get('营养建议') or result.get('建议', '暂无营养建议')
                })
            
            return jsonify(formatted_result)
            
        except Exception as e:
            print(f"分析meals时出错: {str(e)}")
            return jsonify({
                '早餐分析': '分析失败，请重试',
                '午餐分析': '分析失败，请重试',
                '晚餐分析': '分析失败，请重试',
                '营养建议': '生成营养建议失败，请重试'
            })
    return render_template('analyze.html')

@app.route('/recipe', methods=['GET', 'POST'])
def recipe():
    if request.method == 'POST':
        try:
            data = request.get_json()
            agent = create_diet_agent(DIET_RECIPE_GENERATOR_ROLE)
            result = generate_recipe(agent, data['recipe_name'], data['location'])
            
            if not result:
                return jsonify({
                    'error': '生成菜谱失败',
                    'ingredients_list': [],
                    'cooking_process': [],
                    'nutritional_analysis': {}
                }), 500
            
            # 格式化返回结果
            formatted_result = {
                'ingredients_list': result.get('ingredients_list', []),
                'cooking_process': result.get('cooking_process', []),
                'nutritional_analysis': result.get('nutritional_analysis', {})
            }
            return jsonify(formatted_result)
        except Exception as e:
            print(f"生成菜谱时出错: {str(e)}")
            return jsonify({
                'error': str(e),
                'ingredients_list': [],
                'cooking_process': [],
                'nutritional_analysis': {}
            }), 500
    return render_template('recipe.html')

def format_cooking_steps(steps_str):
    """格式化烹饪步骤"""
    if not steps_str:
        return []
    # 将文本分割成步骤列表
    steps = steps_str.split('\n')
    # 清理每个步骤并移除空步骤
    formatted_steps = []
    for i, step in enumerate(steps, 1):
        step = step.strip()
        if step:
            # 移除可能存在的序号前缀
            step = re.sub(r'^\d+[.、]\s*', '', step)
            formatted_steps.append(f"{i}. {step}")
    return formatted_steps

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/save_profile', methods=['POST'])
def save_profile():
    data = request.get_json()
    
    # 计算 BMI
    height_m = data['height'] / 100
    bmi = data['weight'] / (height_m * height_m)
    
    # 使用更科学的Harris-Benedict公式计算基础代谢率(BMR)
    if data['gender'] == 'male':
        bmr = 66 + (13.7 * data['weight']) + (5 * data['height']) - (6.8 * data['age'])
    else:
        bmr = 655 + (9.6 * data['weight']) + (1.8 * data['height']) - (4.7 * data['age'])
    
    # 根据活动水平调整每日所需热量 (PAL - Physical Activity Level)
    activity_factors = {
        'low': 1.2,        # 久坐不运动：BMR x 1.2
        'moderate': 1.375,  # 轻度活动（每周运动1-3次）：BMR x 1.375
        'active': 1.55,    # 中度活动（每周运动3-5次）：BMR x 1.55
        'very_active': 1.725, # 高度活动（每周运动6-7次）：BMR x 1.725
        'extra_active': 1.9   # 极度活动（运动员级别）：BMR x 1.9
    }
    
    daily_calories = bmr * activity_factors[data['activity']]
    
    # 根据健康目标和BMI调整热量
    def calculate_goal_calories(base_calories, bmi, goal):
        if goal == 'lose_weight':
            if bmi > 28:  # 肥胖
                return base_calories * 0.7  # 严格热量限制
            elif bmi > 24:  # 超重
                return base_calories * 0.8  # 适度热量限制
            else:
                return base_calories * 0.9  # 轻度热量限制
        elif goal == 'gain_muscle':
            if bmi < 18.5:  # 体重过低
                return base_calories * 1.3  # 显著增加热量
            else:
                return base_calories * 1.15  # 适度增加热量
        else:  # maintain
            return base_calories

    daily_calories = calculate_goal_calories(daily_calories, bmi, data['health_goal'])
    
    # 确保最低热量摄入标准
    min_calories = 1200 if data['gender'] == 'female' else 1500
    daily_calories = max(daily_calories, min_calories)
    
    # 根据年龄额外调整
    if data['age'] > 60:
        daily_calories *= 0.9  # 老年人基础代谢率降低
    elif data['age'] < 18:
        daily_calories *= 1.1  # 青少年需要额外能量支持生长发育
    
    # 生成营养素分配建议
    nutrition_ratio = {
        'lose_weight': {
            'protein': 0.30,  # 30% 蛋白质
            'fat': 0.25,      # 25% 脂肪
            'carbs': 0.45     # 45% 碳水化合物
        },
        'maintain': {
            'protein': 0.20,  # 20% 蛋白质
            'fat': 0.30,      # 30% 脂肪
            'carbs': 0.50     # 50% 碳水化合物
        },
        'gain_muscle': {
            'protein': 0.35,  # 35% 蛋白质
            'fat': 0.25,      # 25% 脂肪
            'carbs': 0.40     # 40% 碳水化合物
        }
    }
    
    goal = data['health_goal']
    daily_nutrition = {
        'protein': (daily_calories * nutrition_ratio[goal]['protein']) / 4,  # 4卡路里/克蛋白质
        'fat': (daily_calories * nutrition_ratio[goal]['fat']) / 9,         # 9卡路里/克脂肪
        'carbs': (daily_calories * nutrition_ratio[goal]['carbs']) / 4      # 4卡路里/克碳水化合物
    }
    
    # 保存用户信息到会话
    session['user_profile'] = data
    session['health_stats'] = {
        'bmi': bmi,
        'bmr': bmr,
        'daily_calories': daily_calories,
        'daily_nutrition': daily_nutrition
    }
    
    return jsonify({
        'bmi': bmi,
        'bmr': bmr,
        'daily_calories': daily_calories,
        'daily_nutrition': {
            'protein': round(daily_nutrition['protein'], 1),
            'fat': round(daily_nutrition['fat'], 1),
            'carbs': round(daily_nutrition['carbs'], 1)
        },
        'nutrition_ratio': nutrition_ratio[goal]
    })


@app.route('/takeout', methods=['GET', 'POST'])
def takeout():
    if request.method == 'POST':
        try:
            data = request.get_json()
            agent = create_diet_agent(TAKEOUT_RECOMMENDATION_ROLE)
            result = generate_takeout_recommendation(
                agent,
                data['takeout_type'],
                data['price'],
                data['location']
            )

            if not result:
                return jsonify({
                    'error': '生成外卖推荐失败',
                    'dishes_list': [],
                    'nutritional_analysis': {}
                }), 500

            # 格式化返回结果
            formatted_result = {
                'dishes_list': result.get('dishes_list', []),
                'nutritional_analysis': result.get('nutritional_analysis', {})
            }
            return jsonify(formatted_result)
        except Exception as e:
            print(f"生成外卖推荐时出错: {str(e)}")
            return jsonify({
                'error': str(e),
                'dishes_list': [],
                'nutritional_analysis': {}
            }), 500
    return render_template('takeout.html')

@app.route('/economical', methods=['GET', 'POST'])
def economical():
    if request.method == 'POST':
        try:
            data = request.get_json()
            agent = create_diet_agent(ECONOMICAL_ROLE)
            result = generate_economical_diet(
                agent,
                data['budget'],
                data['location'],
                data.get('health_goal', ''),
                data.get('dietary_preferences', '')
            )

            if not result:
                return jsonify({
                    'error': '生成经济型饮食推荐失败',
                    '早餐推荐': {},
                    '午餐推荐': {},
                    '晚餐推荐': {},
                    '省钱建议': [],
                    '总费用': 0.0
                }), 500

            # 格式化返回结果
            formatted_result = {
                '早餐推荐': result.get('早餐推荐', {}),
                '午餐推荐': result.get('午餐推荐', {}),
                '晚餐推荐': result.get('晚餐推荐', {}),
                '省钱建议': result.get('省钱建议', []),
                '总费用': result.get('总费用', 0.0)
            }
            return jsonify(formatted_result)
        except Exception as e:
            print(f"生成经济型饮食推荐时出错: {str(e)}")
            return jsonify({
                'error': str(e),
                '早餐推荐': {},
                '午餐推荐': {},
                '晚餐推荐': {},
                '省钱建议': [],
                '总费用': 0.0
            }), 500
    return render_template('economical.html')

if __name__ == '__main__':
    app.run(debug=True)