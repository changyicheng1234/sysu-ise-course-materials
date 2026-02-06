from agent_config import init_agent_factory

# 健康食谱推荐助手角色
SMART_DIET_ROLE = """
作为健康食谱推荐助手，你专注于根据用户的个人健康信息、饮食偏好和营养需求，提供个性化的食谱建议。
当用户咨询关于健康饮食、营养搭配或特定健康目标的问题时，你将利用百度Agently技术，结合用户的具体情况，给出专业的解答。
你会详细介绍如何根据用户的健康目标（如减重、增肌、控制血糖等）来调整饮食结构，并提供相应的食谱规划和营养建议。
在用户对特定食材或食物有疑问时，你会提供详细的食物营养成分信息，以及它们如何适应用户的健康计划。
对于用户的饮食偏好，你会尊重并考虑在内，推荐既能满足口味又能达到健康目标的食谱。
在用户要求的健康目标与饮食习惯不符合时，你要以健康目标为准，根据健康饮食规范及时调整用户的错误饮食习惯。
你还要监测用户的饮食进度，根据用户的反馈和身体变化，动态调整食谱推荐，确保用户始终获得最合适的健康饮食方案。
注意：在回答时，要确保信息的科学性和准确性，同时保持沟通的亲和力和易于理解。
回答不能出现差错，并且要表述准确，避免歧义和误导。
"""

# 健康食谱分析助手角色
DIET_ANALYZE_ROLE = """
作为健康食谱分析助手，你专注于根据用户的健康目标、生活习惯以及一天三餐的输入，分析其中的营养成分。
你将利用百度Agently技术，结合膳食金字塔和用户的健康目标，提供专业的营养分析和饮食建议。
你要详细介绍每餐的营养成分，收集并分析具体的食物分量（如“200克鸡肉”或“一杯牛奶”），指出用户饮食中可能存在的不足或过剩。
针对用户的一日三餐，给出具体的营养指标建议（如每日蛋白质需求量、维生素摄入量等），并提供改善建议。
你还要考虑到用户的个人健康信息和饮食偏好，并在两方面有矛盾时进行适当平衡，保证建议可以促进用户达成健康目标。
针对用户的不良习惯，提供科学、易于理解、具体且个性化的饮食建议。
注意：回答应易于理解，保持沟通亲和力，不要显得过于AI化。
"""

# 菜谱生成助手角色
DIET_RECIPE_GENERATOR_ROLE = """
分析食谱需求：根据用户输入的食谱名称和所在地，分析 分析可能需要的食材和烹饪方法，同时充分考虑地方特色并结合到烹饪指导中。
生成食材列表：为用户创建一份包含所有必要食材，并提供食材的营养信息。
提供烹饪指导：结合用户所在地的地域特色，给出详细的菜谱制作流程，确保用户能够按照步骤制作出美味的健康菜肴。
营养分析：对生成的菜谱进行全面的营养分析，包括热量、蛋白质、脂肪、维生素和矿物质含量等，帮助用户了解食物的营养价值。
"""

# 外卖推荐助手角色
TAKEOUT_RECOMMENDATION_ROLE = """
作为外卖推荐助手，你专注于根据用户输入的外卖类型、口味偏好、价格预算和所在地区，推荐健康的本地外卖菜品。
你将利用百度Agently技术，结合用户的需求和所在地区的餐饮特色，提供个性化的外卖建议。
推荐的菜品应包括菜品名称、预计价格，并确保符合用户的口味偏好和健康饮食原则。
为每份推荐菜品提供详细的营养分析，包括热量、蛋白质、脂肪和碳水化合物含量。
如果用户的价格预算较低，优先推荐性价比高且营养均衡的菜品。
注意：推荐的菜品应尽量贴合当地外卖平台的实际供应情况，保持建议的实用性和可操作性。
回答必须使用中文，信息科学准确，表述亲和易懂，避免歧义和误导。
"""

# 经济饮食助手角色
ECONOMICAL_ROLE = """
作为经济饮食助手，你专注于在保证饮食相对健康的前提下，为用户提供最经济实惠的饮食建议。
你将利用百度Agently技术，结合用户的预算、饮食偏好、所在地区和健康目标，推荐低成本但营养均衡的饮食方案。
根据用户的预算限制，优先选择价格低廉、易获取的食材，并确保推荐的饮食方案符合健康饮食原则。
你会提供详细的食材选择建议，包括具体份量（如“200克土豆”或“100克鸡胸肉”）和采购建议（如选择当季蔬菜或批发市场购买）。
针对用户的健康目标（如减重、增肌或维持健康），提供性价比高的食谱规划和营养搭配建议，确保营养均衡。
当用户的饮食偏好与预算或健康目标冲突时，以健康目标和预算优先，调整推荐方案并解释原因。
你还会提供省钱小贴士，如如何利用剩余食材、批量购买或自制替代高价加工食品。
注意：推荐的食材和菜谱应贴合用户所在地的市场价格和供应情况，确保实用性和可操作性。
回答必须使用中文，信息科学准确，表述亲和易懂，避免歧义和误导。
"""



def create_diet_agent(role):
    """创建指定角色的代理"""
    agent_factory = init_agent_factory()
    return agent_factory.create_agent().set_role(role)

def query_diet_definition(agent):
    """查询健康饮食定义"""
    result = (
        agent
        .general("输出规定", "必须使用中文进行输出")
        .role({"姓名": "Agently健康饮食小助手", "任务": "使用自己的知识为用户解答常见问题"})
        .user_info("和你对话的用户是一个希望改善自己饮食的人")
        .input({
            "question": "请问健康饮食的定义是什么？",
            "reply_style_expect": "请用对健康饮食一点都不了解的人能理解的方式进行回复"
        })
        .instruct(["请使用{reply_style_expect}的回复风格，回复{question}提出的问题"])
        .output({
            "reply": ("str", "对{question}的直接回复"),
            "next_questions": ([("str", "根据{reply}内容，结合{user_info}提供的用户信息，给用户推荐的可以进一步提问的问题")], "不少于3个")
        })
        .start()
    )
    return result

def generate_diet_recommendation(agent, health_goal=None, dietary_preferences=None, 
                               lifestyle=None, daily_calories=2000, daily_nutrition=None,
                               bmi=None, gender=None, age=None):
    """
    生成个性化的饮食推荐
    """
    daily_nutrition = daily_nutrition or {}
    total_calories = daily_calories or 2000
    
    # 计算每餐分配的热量
    breakfast_calories = total_calories * 0.3  # 早餐30%
    lunch_calories = total_calories * 0.4      # 午餐40%
    dinner_calories = total_calories * 0.3     # 晚餐30%
    
    try:
        result = (
            agent
            .input({
                "user_info": {
                    "gender": gender or "未指定",
                    "age": age or "未指定",
                    "bmi": bmi or "未指定",
                    "health_goal": health_goal or "未指定",
                    "dietary_preferences": dietary_preferences or "未指定",
                    "lifestyle": lifestyle or "未指定"
                },
                "calories": {
                    "total": total_calories,
                    "breakfast": breakfast_calories,
                    "lunch": lunch_calories,
                    "dinner": dinner_calories
                }
            })
            .instruct(
                "请根据用户信息和卡路里需求生成一日三餐推荐。"
                "每餐必须包含：具体推荐的食物及份量清单、食物的详细营养价值分析、具体的食用建议。"
                "确保推荐的食物符合用户的健康目标和饮食偏好，满足每餐的热量需求，"
                "营养均衡且含有适量的蛋白质、碳水化合物和脂肪，并提供具体的食物份量。"
            )
            .output({
                "breakfast": {
                    "foods": ("list", "早餐推荐的具体食物及份量清单"),
                    "nutrition": ("str", "早餐食物的营养价值分析"),
                    "advice": ("str", "早餐的具体食用建议")
                },
                "lunch": {
                    "foods": ("list", "午餐推荐的具体食物及份量清单"),
                    "nutrition": ("str", "午餐食物的营养价值分析"),
                    "advice": ("str", "午餐的具体食用建议")
                },
                "dinner": {
                    "foods": ("list", "晚餐推荐的具体食物及份量清单"),
                    "nutrition": ("str", "晚餐食物的营养价值分析"),
                    "advice": ("str", "晚餐的具体食用建议")
                },
                "nutrition_advice": ("str", "全天营养搭配建议")
            })
            .start()
        )
        
        # 格式化返回结果
        formatted_result = {
            '早餐推荐': {
                '推荐食物': result.get('breakfast', {}).get('foods', []),
                '营养价值': result.get('breakfast', {}).get('nutrition', ''),
                '食用建议': result.get('breakfast', {}).get('advice', '')
            },
            '午餐推荐': {
                '推荐食物': result.get('lunch', {}).get('foods', []),
                '营养价值': result.get('lunch', {}).get('nutrition', ''),
                '食用建议': result.get('lunch', {}).get('advice', '')
            },
            '晚餐推荐': {
                '推荐食物': result.get('dinner', {}).get('foods', []),
                '营养价值': result.get('dinner', {}).get('nutrition', ''),
                '食用建议': result.get('dinner', {}).get('advice', '')
            }
        }

        if 'nutrition_advice' in result:
            formatted_result['营养建议'] = result['nutrition_advice']
        
        return formatted_result
        
    except Exception as e:
        print(f"生成推荐时出错: {e}")
        return {
            '早餐推荐': {'推荐食物': ['生成失败'], '营养价值': '暂无数据', '食用建议': '请稍后重试'},
            '午餐推荐': {'推荐食物': ['生成失败'], '营养价值': '暂无数据', '食用建议': '请稍后重试'},
            '晚餐推荐': {'推荐食物': ['生成失败'], '营养价值': '暂无数据', '食用建议': '请稍后重试'}
        }

def analyze_meals(agent, meals):
    """分析一日三餐的营养情况"""
    try:
        result = (
            agent
            .input(meals)
            .instruct(
                "请详细分析用户提供的三餐饮食情况，要求："
                "1. 对每餐的营养构成进行评估"
                "2. 指出存在的问题和不足"
                "3. 提供具体、可操作的改进建议"
                "4. 确保分析内容详细且易于理解"
            )
            .output({
                "早餐分析": ("str", "早餐的详细分析"),
                "午餐分析": ("str", "午餐的详细分析"),
                "晚餐分析": ("str", "晚餐的详细分析"),
                "营养建议": ("str", "基于三餐分析的综合建议")
            })
            .start()
        )
        
        if not result:
            raise ValueError("分析生成失败")
            
        return result
        
    except Exception as e:
        print(f"分析meals时出错: {str(e)}")
        return {
            "早餐分析": "分析失败，请重试",
            "午餐分析": "分析失败，请重试",
            "晚餐分析": "分析失败，请重试",
            "营养建议": "暂时无法生成营养建议，请重试"
        }

def provide_diet_advice(agent, nutritional_analysis, health_goal, dietary_preferences):
    """提供饮食建议"""
    result = (
        agent
        .input({
            "nutritional_analysis": nutritional_analysis,
            "health_goal": health_goal,
            "dietary_preferences": dietary_preferences
        })
        .instruct(
            "基于用户的营养分析和健康目标，提供改进建议。"
            "建议应包括直观可量化的营养指标（如每日需摄入多少量蛋白质），以及具体的食物推荐（如'每天一杯酸奶'或'增加一小碗约200克蔬菜'）。"
            "保持建议内容自然、亲和力强，不显得过于AI化。"
        )
        .output({"advice": ("str",)})
        .start()
    )
    return result

def generate_recipe(agent, recipe_name, location):
    """生成菜谱"""
    try:
        if not recipe_name or not location:
            raise ValueError("菜品名称和地点不能为空")

        print(f"开始生成菜谱: {recipe_name}, 地点: {location}")
        
        result = (
            agent
            .input({
                "recipe_name": recipe_name, 
                "location": location,
                "requirements": {
                    "ingredients": "需要精确的数量单位",
                    "steps": "需要详细的时间和方法",
                    "nutrition": "需要具体的数值"
                }
            })
            .instruct(
                f"请生成一份{location}地区特色的{recipe_name}的详细菜谱，要求："
                "1. 食材用量必须精确到克或个数（如：2个鸡蛋、200克西红柿）"
                "2. 烹饪步骤必须包含具体时间（如：翻炒2分钟）"
                "3. 营养成分必须给出准确数值（如：180千卡）"
            )
            .output({
                "ingredients_list": [
                    {
                        "name": ("str", "食材名称"),
                        "quantity": ("str", "具体用量，如'2个'或'200克'")
                    }
                ],
                "cooking_process": [("str", "具体的烹饪步骤")],
                "nutritional_analysis": {
                    "calories": ("float", "总热量(千卡)"),
                    "protein": ("float", "蛋白质(克)"),
                    "fat": ("float", "脂肪(克)"),
                    "carbs": ("float", "碳水化合物(克)")
                }
            })
            .start()
        )

        print("API返回结果:", result)  # 添加日志

        if not result:
            raise ValueError("API返回为空")

        # 验证和规范化数据
        ingredients = []
        for item in result.get('ingredients_list', []):
            if isinstance(item, dict) and 'name' in item and 'quantity' in item:
                ingredients.append({
                    'name': str(item['name']),
                    'quantity': str(item['quantity'])
                })
        
        if not ingredients:
            ingredients = [
                {'name': '鸡蛋', 'quantity': '2个'},
                {'name': '西红柿', 'quantity': '200克'},
                {'name': '食用油', 'quantity': '10毫升'},
                {'name': '盐', 'quantity': '2克'}
            ]

        cooking_steps = result.get('cooking_process', [])
        if not cooking_steps:
            cooking_steps = [
                '1. 将西红柿洗净切块，鸡蛋打散',
                '2. 锅中放入5毫升油烧热，倒入鸡蛋液翻炒1分钟至凝固',
                '3. 加入西红柿块翻炒2-3分钟至软化',
                '4. 加入2克盐调味即可'
            ]

        nutrition = result.get('nutritional_analysis', {})
        default_nutrition = {
            'calories': 180.0,
            'protein': 12.0,
            'fat': 8.0,
            'carbs': 6.0
        }

        for key in default_nutrition:
            if key not in nutrition or not isinstance(nutrition[key], (int, float)):
                nutrition[key] = default_nutrition[key]

        return {
            'ingredients_list': ingredients,
            'cooking_process': cooking_steps,
            'nutritional_analysis': nutrition
        }

    except Exception as e:
        print(f"生成菜谱时出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        
        # 返回默认值
        return {
            'ingredients_list': [
                {'name': '鸡蛋', 'quantity': '2个'},
                {'name': '西红柿', 'quantity': '200克'},
                {'name': '食用油', 'quantity': '10毫升'},
                {'name': '盐', 'quantity': '2克'}
            ],
            'cooking_process': [
                '1. 将西红柿洗净切块，鸡蛋打散',
                '2. 锅中放入5毫升油烧热，倒入鸡蛋液翻炒1分钟至凝固',
                '3. 加入西红柿块翻炒2-3分钟至软化',
                '4. 加入2克盐调味即可'
            ],
            'nutritional_analysis': {
                'calories': 180.0,
                'protein': 12.0,
                'fat': 8.0,
                'carbs': 6.0
            }
        }


def generate_takeout_recommendation(agent, takeout_type, price, location):
    """生成外卖推荐"""
    try:
        if not takeout_type or not price or not location:
            raise ValueError("外卖类型、价格和地点不能为空")

        print(f"开始生成外卖推荐: 类型={takeout_type}, 价格={price}, 地点={location}")

        result = (
            agent
            .input({
                "takeout_type": takeout_type,
                "price": price,
                "location": location,
                "requirements": {
                    "dishes": "需要菜品名称和预计价格",
                    "nutrition": "需要具体的营养数值"
                }
            })
            .instruct(
                f"请根据用户输入的外卖类型'{takeout_type}'、价格预算'{price}'和所在地'{location}'，推荐3-5种健康的外卖菜品，要求："
                "1. 每种菜品包括名称和预计价格（如：宫保鸡丁，约25元）"
                "2. 推荐菜品需符合用户的口味偏好和健康饮食原则"
                "3. 提供每种菜品的营养分析，包括热量（千卡）、蛋白质（克）、脂肪（克）、碳水化合物（克）"
                "4. 优先选择符合价格预算且营养均衡的菜品"
                "5. 考虑'{location}'地区的餐饮特色和外卖平台供应情况"
            )
            .output({
                "dishes_list": [
                    {
                        "name": ("str", "菜品名称"),
                        "price": ("str", "预计价格，如'约25元'")
                    }
                ],
                "nutritional_analysis": {
                    "calories": ("float", "总热量(千卡)"),
                    "protein": ("float", "蛋白质(克)"),
                    "fat": ("float", "脂肪(克)"),
                    "carbs": ("float", "碳水化合物(克)")
                }
            })
            .start()
        )

        print("API返回结果:", result)

        if not result:
            raise ValueError("API返回为空")

        # 验证和规范化数据
        dishes = []
        for item in result.get('dishes_list', []):
            if isinstance(item, dict) and 'name' in item and 'price' in item:
                dishes.append({
                    'name': str(item['name']),
                    'price': str(item['price'])
                })

        if not dishes:
            dishes = [
                {'name': '清蒸鲈鱼', 'price': '约35元'},
                {'name': '宫保鸡丁', 'price': '约25元'},
                {'name': '素炒时蔬', 'price': '约15元'}
            ]

        nutrition = result.get('nutritional_analysis', {})
        default_nutrition = {
            'calories': 500.0,
            'protein': 30.0,
            'fat': 20.0,
            'carbs': 50.0
        }

        for key in default_nutrition:
            if key not in nutrition or not isinstance(nutrition[key], (int, float)):
                nutrition[key] = default_nutrition[key]

        return {
            'dishes_list': dishes,
            'nutritional_analysis': nutrition
        }

    except Exception as e:
        print(f"生成外卖推荐时出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

        # 返回默认值
        return {
            'dishes_list': [
                {'name': '清蒸鲈鱼', 'price': '约35元'},
                {'name': '宫保鸡丁', 'price': '约25元'},
                {'name': '素炒时蔬', 'price': '约15元'}
            ],
            'nutritional_analysis': {
                'calories': 500.0,
                'protein': 30.0,
                'fat': 20.0,
                'carbs': 50.0
            }
        }

def generate_economical_diet(agent, budget, location, health_goal=None, dietary_preferences=None):
    """生成经济型饮食推荐"""
    try:
        if not budget or not location:
            raise ValueError("预算和地点不能为空")

        print(f"开始生成经济型饮食推荐: 预算={budget}, 地点={location}")

        result = (
            agent
            .input({
                "budget": budget,
                "location": location,
                "health_goal": health_goal or "未指定",
                "dietary_preferences": dietary_preferences or "未指定",
                "requirements": {
                    "meals": "每日三餐的食材清单和预算分配",
                    "nutrition": "每餐的营养分析",
                    "tips": "省钱采购和烹饪建议"
                }
            })
            .instruct(
                f"请根据用户预算'{budget}'、所在地'{location}'、健康目标和饮食偏好，生成一日三餐的经济型饮食推荐，要求："
                "1. 每餐推荐具体食材和份量（如‘200克土豆’），并确保总费用在预算范围内"
                "2. 提供每餐的营养分析，包括热量、蛋白质、脂肪和碳水化合物含量"
                "3. 确保推荐的食材易获取、价格低廉，并符合健康饮食原则"
                "4. 提供省钱小贴士，如选择当季食材、批量购买或利用剩余食材"
                "5. 考虑'{location}'地区的市场价格和食材供应情况"
            )
            .output({
                "breakfast": {
                    "foods": ("list", "早餐推荐的具体食材及份量清单"),
                    "cost": ("float", "早餐预计费用（元）"),
                    "nutrition": ("str", "早餐的营养价值分析")
                },
                "lunch": {
                    "foods": ("list", "午餐推荐的具体食材及份量清单"),
                    "cost": ("float", "午餐预计费用（元）"),
                    "nutrition": ("str", "午餐的营养价值分析")
                },
                "dinner": {
                    "foods": ("list", "晚餐推荐的具体食材及份量清单"),
                    "cost": ("float", "晚餐预计费用（元）"),
                    "nutrition": ("str", "晚餐的营养价值分析")
                },
                "saving_tips": ("list", "省钱采购和烹饪建议"),
                "total_cost": ("float", "全天饮食总费用（元）")
            })
            .start()
        )

        print("API返回结果:", result)

        if not result:
            raise ValueError("API返回为空")

        # 验证和规范化数据
        meals = ["breakfast", "lunch", "dinner"]
        formatted_result = {}
        total_cost = 0.0

        for meal in meals:
            meal_data = result.get(meal, {})
            foods = meal_data.get("foods", [])
            cost = meal_data.get("cost", 0.0)
            nutrition = meal_data.get("nutrition", "暂无数据")

            if not foods:
                foods = [
                    {"name": "鸡蛋", "quantity": "2个"},
                    {"name": "土豆", "quantity": "200克"}
                ]
            if not isinstance(cost, (int, float)):
                cost = 5.0

            total_cost += cost
            formatted_result[meal] = {
                "foods": foods,
                "cost": cost,
                "nutrition": nutrition
            }

        saving_tips = result.get("saving_tips", [])
        if not saving_tips:
            saving_tips = [
                "选择当季蔬菜以降低成本",
                "批量购买鸡蛋和米面类食材",
                "利用剩余食材制作杂烩汤"
            ]

        total_cost = result.get("total_cost", total_cost)
        if not isinstance(total_cost, (int, float)):
            total_cost = sum([formatted_result[meal]["cost"] for meal in meals])

        return {
            "早餐推荐": {
                "推荐食材": formatted_result["breakfast"]["foods"],
                "预计费用": formatted_result["breakfast"]["cost"],
                "营养价值": formatted_result["breakfast"]["nutrition"]
            },
            "午餐推荐": {
                "推荐食材": formatted_result["lunch"]["foods"],
                "预计费用": formatted_result["lunch"]["cost"],
                "营养价值": formatted_result["lunch"]["nutrition"]
            },
            "晚餐推荐": {
                "推荐食材": formatted_result["dinner"]["foods"],
                "预计费用": formatted_result["dinner"]["cost"],
                "营养价值": formatted_result["dinner"]["nutrition"]
            },
            "省钱建议": saving_tips,
            "总费用": total_cost
        }

    except Exception as e:
        print(f"生成经济型饮食推荐时出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

        # 返回默认值
        return {
            "早餐推荐": {
                "推荐食材": [{"name": "鸡蛋", "quantity": "2个"}, {"name": "面包", "quantity": "2片"}],
                "预计费用": 5.0,
                "营养价值": "热量：200千卡，蛋白质：12克，脂肪：8克，碳水化合物：20克"
            },
            "午餐推荐": {
                "推荐食材": [{"name": "土豆", "quantity": "200克"}, {"name": "鸡胸肉", "quantity": "100克"}],
                "预计费用": 8.0,
                "营养价值": "热量：350千卡，蛋白质：25克，脂肪：5克，碳水化合物：40克"
            },
            "晚餐推荐": {
                "推荐食材": [{"name": "白菜", "quantity": "200克"}, {"name": "豆腐", "quantity": "100克"}],
                "预计费用": 4.0,
                "营养价值": "热量：150千卡，蛋白质：10克，脂肪：3克，碳水化合物：15克"
            },
            "省钱建议": [
                "选择当季蔬菜以降低成本",
                "批量购买鸡蛋和米面类食材",
                "利用剩余食材制作杂烩汤"
            ],
            "总费用": 17.0
        }