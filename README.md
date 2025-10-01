# Newport Centurions Korfball Club Website - newportcenturions.co.uk

Professional Jekyll-powered website for Newport Centurions Korfball Club, featuring modern design, comprehensive SEO optimization, and Progressive Web App capabilities.

## 🏃 Quick Start

```bash
# Install dependencies
bundle install

# Run development server
./dev.sh
# or
bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload

# Build for production
./build.sh
# or
bundle exec jekyll build
```

## 🛠️ Tech Stack

- **Static Site Generator**: Jekyll 3.10.0
- **Hosting**: GitHub Pages
- **CSS Framework**: Custom CSS with modern features
- **Icons**: Font Awesome 6.4.0
- **Image Format**: WebP with fallbacks
- **Performance**: Service Worker, Critical CSS, DNS Prefetch
- **SEO**: Enhanced structured data, comprehensive meta tags

## 📁 Project Structure

```
newportcenturions.co.uk/
├── _config.yml              # Jekyll configuration
├── _layouts/
│   └── default.html         # Main layout with SEO optimization
├── _includes/
│   ├── footer.html
│   ├── header.html
│   ├── navigation.html
│   └── social-links.html
├── assets/
│   ├── css/
│   │   ├── critical.css     # Critical path CSS
│   │   └── styles.css       # Main stylesheet
│   └── favicon/             # Comprehensive favicon set
├── images/
│   └── *.webp              # Optimized WebP images
├── pages/
│   ├── index.md            # Homepage
│   ├── about.md            # About the club
│   ├── join.md             # Join us page
│   ├── contact.md          # Contact form
│   ├── social.md           # Social media page
│   ├── support.md          # Support/fundraising
│   └── what-is-korfball.md # Sport information
├── sw.js                   # Service Worker for PWA
├── manifest.json           # Web App Manifest
├── robots.txt              # SEO crawler instructions
├── sitemap.xml             # Enhanced XML sitemap
├── feed.xml                # RSS feed
├── .htaccess               # Server configuration
├── build.sh                # Production build script
└── dev.sh                  # Development server script
```

## 🔍 SEO Features

### **Technical SEO**
- ✅ Comprehensive structured data (Organization, SportsTeam, WebSite schemas)
- ✅ Enhanced meta tags and Open Graph optimization
- ✅ XML sitemap with image schemas and priorities
- ✅ RSS feed for content syndication
- ✅ Robots.txt with specific crawler instructions
- ✅ DNS prefetch for performance optimization

### **Performance Optimization**
- ✅ Critical CSS inlining for faster rendering
- ✅ Service Worker for offline functionality
- ✅ Progressive Web App (PWA) capabilities
- ✅ WebP image format with fallbacks
- ✅ Comprehensive browser caching strategies
- ✅ Security headers and HSTS implementation

### **Accessibility & UX**
- ✅ Skip links for keyboard navigation
- ✅ ARIA labels and semantic HTML
- ✅ Screen reader optimization
- ✅ Mobile-first responsive design
- ✅ Enhanced focus indicators
- ✅ Print-friendly styling

## 📱 Pages & Features

### **Main Pages**
- **Homepage** (`/`) - Club overview with training information
- **About Us** (`/about/`) - Club history and achievements
- **Join Us** (`/join-us/`) - Membership information and process
- **What is Korfball?** (`/what-is-korfball/`) - Sport introduction
- **Contact** (`/contact/`) - Contact form and information
- **Support Us** (`/support/`) - Fundraising and sponsorship
- **Team Store** (external) - Official korfball kit and merchandise

### **Enhanced Features**
- 📱 **Progressive Web App** - Installable mobile experience
- 📧 **Contact Form** - Netlify-compatible with validation
- 🔄 **Offline Support** - Service Worker caching
- 📈 **Analytics** - Google Analytics integration
- 🎨 **Modern Design** - Glass morphism and 2025 aesthetics
- 🚀 **Performance** - Optimized for Core Web Vitals

## 📱 Social Media Links

- **Facebook**: [@newportcenturions](https://facebook.com/newportcenturions)
- **Twitter**: [@newportkorfball](https://twitter.com/newportkorfball)
- **Instagram**: [@newportkorfball](https://instagram.com/newportkorfball)
- **YouTube**: [@newportcenturionskorfball5878](https://youtube.com/@newportcenturionskorfball5878)

## 🚀 Deployment

### **GitHub Pages (Automatic)**
The site automatically deploys to GitHub Pages when changes are pushed to the main branch.

### **Manual Deployment**
```bash
# Build the site
./build.sh

# The _site/ directory contains the built website
# Upload contents to your web server
```

### **Local Development**
```bash
# Start development server
./dev.sh

# Access at http://localhost:4000
# Live reload enabled for real-time changes
```

## 🧰 Development Requirements

- **Ruby**: >= 2.7.0
- **Bundler**: >= 2.0.0
- **Jekyll**: ~> 3.10.0
- **Node.js**: (optional, for additional tooling)

## 🔧 Configuration

### **Site Settings** (`_config.yml`)
- SEO configuration and meta tags
- Navigation menu structure
- Social media links
- Organization schema data
- Plugin settings

### **Build Scripts**
- `build.sh` - Production build with optimization
- `dev.sh` - Development server with live reload

## 📊 Performance Features

### **Core Web Vitals Optimization**
- ⚡ **First Contentful Paint**: Optimized with critical CSS
- 🎯 **Largest Contentful Paint**: Image optimization and caching
- 📱 **Cumulative Layout Shift**: Stable layouts with proper sizing
- 🖱️ **First Input Delay**: Efficient JavaScript and lazy loading

### **PWA Capabilities**
- 📱 Installable as mobile app
- 🔄 Offline functionality
- 🔔 Push notification support (ready)
- 📋 Background sync capabilities

## 🛡️ Security Features

- 🔒 **HTTPS Enforcement** via .htaccess
- 🛡️ **Security Headers** (HSTS, CSP, X-Frame-Options)
- 🔐 **Content Security Policy** implementation
- 📝 **Security.txt** for responsible disclosure

## 📄 License

© 2025 Newport Centurions Korfball Club. All rights reserved.

---

**Welsh League Champions 2022/2023 & 2025** 🏆

For questions or contributions, please [contact us](/contact/) or open an issue on GitHub.

<a href="https://www.buymeacoffee.com/darthvader666uk" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>