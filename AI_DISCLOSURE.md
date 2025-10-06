# AI Usage Disclosure
## NASA Space Apps Challenge 2025 - AI Tool Compliance

This document provides full transparency regarding the use of Artificial Intelligence (AI) tools in the development of the **NASA BioExplorer** project, in compliance with NASA Space Apps Challenge guidelines.

---

## 🤖 AI Tools Used

### 1. **Lovable** (AI-Powered Development Platform)
- **Purpose**: Base web application template and initial project scaffolding
- **Scope**: 
  - Frontend application structure
  - React + TypeScript setup
  - UI component library integration (shadcn/ui)
  - Initial routing and page layouts
  - Tailwind CSS configuration
- **Extent**: Generated the foundational frontend codebase structure

### 2. **Windsurf** and **ChatGPT** (AI Code Assistant)
- **Purpose**: Feature implementation and code development
- **Scope**:
  - Feature implementation across frontend and backend
  - Code completion and suggestions
  - Bug fixing and debugging assistance
  - API integration logic
  - Component development
- **Extent**: Assisted with iterative development and feature additions throughout the project

### 3. **AI Image Generation** (Generative AI Tool)
- **Purpose**: Landing page header image creation
- **Scope**: Space-themed hero image for the landing page
- **File**: `/frontend/src/assets/space-hero.jpg`
- **Disclosure**: Image is watermarked with "AI GENERATED" as per NASA requirements

---

## 📂 Affected Project Components

### **Frontend Code** (`/frontend`)
- **AI-Assisted Files**:
  - All TypeScript/React components (`.tsx` files)
  - UI component configurations
  - Styling and layout code
  - Routing and navigation logic
  - Authentication flows
- **Tools Used**: Lovable (initial generation), Windsurf (feature development)
- **Human Contribution**: Architecture decisions, feature specifications, customization, integration, testing

### **Backend Code** (`/backend`)
- **AI-Assisted Files**:
  - RAG (Retrieval-Augmented Generation) pipeline
  - API endpoints
  - LLM integration logic
  - Data fetching scripts
- **Tools Used**: ChatGPT (development assistance)
- **Human Contribution**: System design, algorithm selection, data processing logic, API design, debugging

### **Images and Visual Assets**
- **File**: `frontend/src/assets/space-hero.jpg`
- **Tool**: AI Image Generation
- **Watermark**: "AI GENERATED" visible watermark added (bottom right)
- **Human Contribution**: Prompt engineering, image selection, integration

---

## 🎨 AI-Generated Content Details

### Images
| File | Type | AI Tool | Watermark | Purpose |
|------|------|---------|-----------|---------|
| `frontend/src/assets/space-hero.jpg` | Image | AI Image Generator | ✓ Yes (visible) | Landing page hero background |

### Code and Data
| Component | AI Tool | Human Oversight | Description |
|-----------|---------|-----------------|-------------|
| Frontend Application | Lovable + Windsurf | Extensive | React/TypeScript UI with custom features |
| Backend API | Windsurf | Extensive | Flask API with RAG pipeline |
| Data Pipeline | ChatGPT | Extensive | NASA data fetching and processing |
| LLM Integration | ChatGPT | Extensive | Langchain-based RAG implementation |

---

## 👨‍💻 Human Contribution & Originality

While AI tools accelerated development, the project demonstrates significant human creativity and technical expertise:

### **Original Contributions**
1. **Project Concept & Architecture**: 
   - Complete system design for NASA bioscience data exploration
   - RAG pipeline architecture for scientific literature
   - User experience and interaction design

2. **Technical Implementation**:
   - Integration of multiple APIs and services
   - Custom RAG pipeline configuration
   - NASA data source selection and processing
   - Database schema and data modeling
   - Authentication and security implementation

3. **Problem Solving**:
   - Debugging and troubleshooting
   - Performance optimization
   - Cross-platform compatibility
   - API endpoint design
   - Error handling and edge cases

4. **Domain Expertise**:
   - Understanding of NASA space biology research
   - Scientific literature processing
   - User requirements for research tools
   - Query optimization for scientific data

### **Development Workflow**
- AI tools provided **code suggestions and scaffolding**
- Human developers provided **direction, specifications, and validation**
- All AI-generated code was **reviewed, tested, and modified** by team members
- Critical logic and algorithms were **designed and verified** by the team

---

## 🔍 Code Review & Quality Assurance

All AI-generated code underwent:
1. **Human review** for correctness and security
2. **Testing** for functionality and edge cases
3. **Modification** to meet specific project requirements
4. **Integration** with manually written components
5. **Optimization** for performance and user experience

---

## 📋 NASA Branding Compliance

✓ **No NASA logos, flags, or mission identifiers** were used or modified by AI tools  
✓ **All NASA-related content** is properly attributed and sourced from public datasets  
✓ **AI-generated images** do not contain or modify NASA branding

---

## 📝 Metadata Tags

**Project Type**: Web Application  
**AI Usage**: Code Generation, Image Generation  
**AI Transparency**: Full Disclosure  
**Compliance Status**: NASA Space Apps Challenge Guidelines Compliant  

---

## 📧 Contact

For questions about AI usage in this project:
- **Repository**: https://github.com/Hackathon-Team-WMU/nasa-space-bio
- **Team**: Hackathon-Team-WMU

---

*Last Updated: October 5, 2025*  
*Document Version: 1.0*
