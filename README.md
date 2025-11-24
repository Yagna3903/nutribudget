# 🥗 NutriBudget

> **Smart grocery planning that balances nutrition and budget**

Making healthy eating affordable for everyone. NutriBudget helps you get the most nutrition for your money by analyzing real grocery data and creating optimized shopping plans.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge)](https://nutribudget-web.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

## 🚀 Try It Live!

**👉 [nutribudget-web.vercel.app](https://nutribudget-web.vercel.app)**

No installation needed - just visit the link and start planning your budget-friendly meals!

---

## What is NutriBudget?

We built NutriBudget after realizing how hard it is to eat healthy on a tight budget. The app takes your budget, dietary preferences, and health goals, then uses machine learning to find the best combination of groceries for you.

**The result?** A shopping list that's nutritious, affordable, and personalized to your needs.

---

## ✨ Features

### 🎯 Smart Planning
- Set your budget and get a complete shopping basket
- Choose your diet: Vegetarian, Non-Vegetarian, or Vegan
- Pick a health goal: Balanced, High Protein, or Low Sugar

### 🤖 AI-Powered
- **Smart Chef**: Get personalized recipes based on your basket (powered by Google Gemini AI)
- Machine learning scores every product for health and value
- Intelligent optimization finds the best products for your needs

### 🗺️ Local Shopper
- Find nearby stores that carry your items
- Direct navigation to your local grocery stores
- Built-in map integration

### 📊 Insights
- See exactly how much nutrition you're getting
- Compare against recommended daily values
- Track how much you're saving vs typical shopping
- Understand the social impact (SDG goals)

### 💾 Export & Share
- Download your shopping list as a text or PDF file
- Share with family members
- Save for weekly planning

---

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 with React
- TypeScript for type safety
- Tailwind CSS for styling
- Framer Motion for smooth animations

**Backend:**
- Flask (Python) REST API
- Pandas for data processing
- Scikit-learn for machine learning
- Google Gemini AI for recipe generation

**Deployment:**
- Frontend: Vercel
- Backend: Render
- Continuous deployment from GitHub

**Data:**
- 4,900+ Canadian grocery products
- Real nutrition facts from Health Canada & USDA
- Price data from major grocery chains

---

## 🏃 Running Locally

Want to run NutriBudget on your own machine? Here's how:

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Backend Setup

```bash
# Navigate to backend folder
cd api

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
echo "GEMINI_API_KEY=your_key_here" > .env

# Start the server
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend folder
cd web

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local

# Start the dev server
npm run dev
```

Frontend runs on `http://localhost:3000`

---


## 🎯 How It Works

### 1. Input Your Details
Tell us your budget, household size, diet type, and health goals.

### 2. Machine Learning Analysis

Our system uses **three trained ML models** working together:

**🤖 Product Quality Classifier** (Random Forest)
- Analyzes nutritional profile to classify products as High/Medium/Low quality
- Trained on 4,900 products
- Considers: protein, fiber, calories vs. sugar, fat, sodium

**📈 Value Predictor** (Random Forest Regression)  
- Predicts nutritional value score based on ingredients
- Identifies products that offer exceptional nutritional value
- Trained with cross-validation for accuracy

**💰 Price Fairness Model** (Linear Regression)
- Predicts fair price based on nutritional content
- Flags underpriced items as "best deals"
- Helps find hidden gems in the grocery store

### 3. Intelligent Selection

The ML-powered optimizer picks the best combination of products that:
- Fits your budget perfectly
- Matches your dietary preferences
- Achieves your health goals
- **Maximizes variety** using cluster-based diversity
- Balances nutrition, cost, and quality

### 4. Get Your Plan

Receive a complete shopping list with:
- Exact products and quantities
- Nutritional breakdown
- Store locations
- AI-generated recipes (powered by Google Gemini)
- Estimated savings

---

## 📱 Screenshots

*The app features a clean, modern interface with:*
- Intuitive budget input form
- Real-time nutrition tracking
- Beautiful data visualizations
- Interactive recipe cards
- Store locator maps

---

## 🌍 Impact

### Contributing to UN Sustainable Development Goals

**SDG 2: Zero Hunger**
- Making nutritious food accessible to budget-constrained families
- Reducing food waste through smart planning
- Helping people maximize their grocery budgets

**SDG 3: Good Health and Well-being**
- Promoting healthy eating habits
- Providing accurate nutritional information
- Enabling informed food choices

---

## 🚧 Roadmap

What's next for NutriBudget:

- [ ] Meal prep guides and cooking instructions
- [ ] Weekly meal planning with recurring orders
- [ ] Allergen tracking and warnings
- [ ] Price history and trend analysis
- [ ] Multi-store comparison
- [ ] User accounts and saved preferences
- [ ] Mobile app (iOS & Android)
- [ ] Integration with online grocery delivery

---

## 🤝 Contributing

We'd love your help making NutriBudget better! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**Good first issues:**
- Adding more dietary restrictions (gluten-free, dairy-free, etc.)
- Improving the ML model accuracy
- Adding support for different countries/currencies
- Writing tests
- Improving documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this project freely, even for commercial purposes. Just keep the copyright notice.

---

## 🙏 Acknowledgments

- Nutrition data sourced from Health Canada and USDA databases
- Inspired by the need to make healthy eating accessible
- Built with love for budget-conscious families everywhere
- Thanks to the open-source community for amazing tools

---

## 📞 Contact & Support

**Found a bug?** Open an issue on GitHub

**Have questions?** Check out our [Deployment Guide](deployment_guide.md)

**Want to contribute?** See the Contributing section above!

---

## ⚠️ Disclaimer

Prices and nutritional information are estimates based on Canadian grocery data (November 2025). Actual prices may vary by location and time. Nutritional data sourced from Health Canada and USDA databases. Always verify with your local store before purchasing.

This tool is for informational purposes and should not replace professional dietary advice. Consult a healthcare provider or registered dietitian for personalized nutrition guidance.

---

<div align="center">

**Made with ❤️ for healthier, more affordable grocery shopping**

[Live Demo](https://nutribudget-web.vercel.app) • [Report Bug](https://github.com/Yagna3903/nutribudget/issues) • [Request Feature](https://github.com/Yagna3903/nutribudget/issues)

</div>
