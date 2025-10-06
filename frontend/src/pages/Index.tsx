/**
 * Landing Page Component
 * 
 * AI Usage Disclosure (NASA Space Apps Challenge 2025):
 * - Component developed with Lovable and Windsurf AI assistance
 * - Hero image (space-hero.jpg) is AI-generated with visible watermark
 * - All code reviewed and customized by human developers
 */

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Rocket, Database, Brain, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import spaceHero from "@/assets/space-hero.jpg";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <div 
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url(${spaceHero})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-b from-background/80 via-background/60 to-background"></div>
        </div>
        
        <div className="relative z-10 container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent animate-fade-in">
            NASA BioExplorer
          </h1>
          <p className="text-xl md:text-2xl text-foreground/90 mb-8 max-w-3xl mx-auto">
            Unlock decades of space biology research with AI-powered exploration. 
            Discover insights from NASA's bioscience experiments for the next era of human space exploration.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/auth">
              <Button size="lg" className="bg-accent hover:bg-accent/90 text-accent-foreground font-semibold px-8 py-6 text-lg">
                Get Started <ArrowRight className="ml-2" />
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="border-primary text-primary hover:bg-primary/10 px-8 py-6 text-lg">
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16">Explore Space Biology</h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <Card className="p-8 bg-card border-border hover:border-primary/50 transition-all hover:scale-105">
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-6">
              <Brain className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-2xl font-semibold mb-4">AI-Powered Search</h3>
            <p className="text-muted-foreground">
              Chat naturally with our AI to find relevant NASA bioscience publications and experiments instantly.
            </p>
          </Card>

          <Card className="p-8 bg-card border-border hover:border-primary/50 transition-all hover:scale-105">
            <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-6">
              <Database className="w-6 h-6 text-accent" />
            </div>
            <h3 className="text-2xl font-semibold mb-4">Comprehensive Database</h3>
            <p className="text-muted-foreground">
              Access decades of space biology research data and experimental results in one unified platform.
            </p>
          </Card>

          <Card className="p-8 bg-card border-border hover:border-primary/50 transition-all hover:scale-105">
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-6">
              <Rocket className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-2xl font-semibold mb-4">Mission Ready</h3>
            <p className="text-muted-foreground">
              Essential insights for Moon and Mars missions, compiled from verified NASA research and experiments.
            </p>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 container mx-auto px-4">
        <Card className="p-12 bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10 border-primary/30">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-4xl font-bold mb-6">Ready to Explore?</h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join researchers and space enthusiasts in discovering the future of human space exploration.
            </p>
            <Link to="/auth">
              <Button size="lg" className="bg-accent hover:bg-accent/90 text-accent-foreground font-semibold px-8 py-6 text-lg">
                Start Exploring <ArrowRight className="ml-2" />
              </Button>
            </Link>
          </div>
        </Card>
      </section>
    </div>
  );
};

export default Index;
