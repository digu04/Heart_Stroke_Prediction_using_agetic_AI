// ============================================
// particles.js — Interactive 3D Particle System
// Dots get closer/denser as user progresses
// ============================================

class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: -1000, y: -1000 };
        this.progress = 0; // 0 to 1 (Register → History)
        this.baseCount = 60;
        this.connectionDistance = 120;
        this.mouseRadius = 180;
        this.animationId = null;

        this.resize();
        this.init();
        this.bindEvents();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    init() {
        this.particles = [];
        const count = this.baseCount + Math.floor(this.progress * 80);
        for (let i = 0; i < count; i++) {
            this.particles.push(this.createParticle());
        }
    }

    createParticle() {
        const depth = Math.random(); // 0 = far, 1 = near
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            z: depth,
            baseRadius: 1 + Math.random() * 2.5,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            vz: (Math.random() - 0.5) * 0.005,
            pulsePhase: Math.random() * Math.PI * 2,
        };
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resize();
            this.init();
        });

        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });

        window.addEventListener('mouseleave', () => {
            this.mouse.x = -1000;
            this.mouse.y = -1000;
        });
    }

    setProgress(step) {
        // step: 0=register, 1=input, 2=results, 3=chat, 4=history
        const target = step / 4;
        // Smooth transition
        const animate = () => {
            const diff = target - this.progress;
            if (Math.abs(diff) > 0.005) {
                this.progress += diff * 0.05;
                requestAnimationFrame(animate);
            } else {
                this.progress = target;
            }
            // Adjust particle count
            const desired = this.baseCount + Math.floor(this.progress * 80);
            while (this.particles.length < desired) {
                this.particles.push(this.createParticle());
            }
            while (this.particles.length > desired + 10) {
                this.particles.pop();
            }
        };
        animate();
    }

    getColor(z) {
        // Color shifts based on progress
        const colors = [
            { r: 51, g: 102, b: 255 },   // blue (register)
            { r: 100, g: 130, b: 255 },   // light blue (input)
            { r: 255, g: 61, b: 113 },    // red (results)
            { r: 155, g: 89, b: 182 },    // purple (chat)
            { r: 0, g: 214, b: 143 },     // green (history)
        ];

        const idx = Math.min(Math.floor(this.progress * 4), 3);
        const next = Math.min(idx + 1, 4);
        const t = (this.progress * 4) - idx;

        const c1 = colors[idx];
        const c2 = colors[next];

        const r = Math.round(c1.r + (c2.r - c1.r) * t);
        const g = Math.round(c1.g + (c2.g - c1.g) * t);
        const b = Math.round(c1.b + (c2.b - c1.b) * t);

        const alpha = 0.15 + z * 0.55;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    getLineColor(z) {
        const colors = [
            { r: 51, g: 102, b: 255 },
            { r: 100, g: 130, b: 255 },
            { r: 255, g: 61, b: 113 },
            { r: 155, g: 89, b: 182 },
            { r: 0, g: 214, b: 143 },
        ];

        const idx = Math.min(Math.floor(this.progress * 4), 3);
        const next = Math.min(idx + 1, 4);
        const t = (this.progress * 4) - idx;

        const c1 = colors[idx];
        const c2 = colors[next];

        const r = Math.round(c1.r + (c2.r - c1.r) * t);
        const g = Math.round(c1.g + (c2.g - c1.g) * t);
        const b = Math.round(c1.b + (c2.b - c1.b) * t);

        const alpha = 0.03 + z * 0.08;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const time = Date.now() * 0.001;
        const connDist = this.connectionDistance + this.progress * 60;

        // Update & draw particles
        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];

            // Depth oscillation
            p.z += p.vz;
            if (p.z <= 0.05 || p.z >= 1) p.vz *= -1;
            p.z = Math.max(0.05, Math.min(1, p.z));

            // Scale factor based on depth + progress
            const depthScale = 0.3 + p.z * 0.7;
            const progressScale = 1 + this.progress * 0.6;
            const scale = depthScale * progressScale;

            // Movement (deeper = slower for parallax)
            p.x += p.vx * depthScale;
            p.y += p.vy * depthScale;

            // Mouse interaction — push particles away gently
            const dx = p.x - this.mouse.x;
            const dy = p.y - this.mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < this.mouseRadius) {
                const force = (1 - dist / this.mouseRadius) * 1.5 * p.z;
                p.x += (dx / dist) * force;
                p.y += (dy / dist) * force;
            }

            // Wrap around edges
            if (p.x < -20) p.x = this.canvas.width + 20;
            if (p.x > this.canvas.width + 20) p.x = -20;
            if (p.y < -20) p.y = this.canvas.height + 20;
            if (p.y > this.canvas.height + 20) p.y = -20;

            // Pulse
            const pulse = 1 + Math.sin(time * 2 + p.pulsePhase) * 0.2;
            const radius = p.baseRadius * scale * pulse;

            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
            this.ctx.fillStyle = this.getColor(p.z);
            this.ctx.fill();

            // Glow for near particles
            if (p.z > 0.7) {
                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, radius * 2.5, 0, Math.PI * 2);
                const glow = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 2.5);
                glow.addColorStop(0, this.getColor(p.z * 0.3));
                glow.addColorStop(1, 'transparent');
                this.ctx.fillStyle = glow;
                this.ctx.fill();
            }

            // Connections (more connections as progress increases)
            for (let j = i + 1; j < this.particles.length; j++) {
                const p2 = this.particles[j];
                const cdx = p.x - p2.x;
                const cdy = p.y - p2.y;
                const cdist = Math.sqrt(cdx * cdx + cdy * cdy);

                if (cdist < connDist) {
                    const avgZ = (p.z + p2.z) / 2;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p.x, p.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.strokeStyle = this.getLineColor(avgZ * (1 - cdist / connDist));
                    this.ctx.lineWidth = 0.5 + avgZ * 0.8;
                    this.ctx.stroke();
                }
            }
        }

        this.animationId = requestAnimationFrame(() => this.animate());
    }

    destroy() {
        if (this.animationId) cancelAnimationFrame(this.animationId);
    }
}

// Initialize when DOM is ready
let particleSystem = null;

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particleCanvas');
    if (canvas) {
        particleSystem = new ParticleSystem(canvas);
    }
});
