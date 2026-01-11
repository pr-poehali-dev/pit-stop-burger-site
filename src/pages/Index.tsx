const Index = () => {
  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      <div 
        className="absolute left-0 top-0 w-[500px] h-[500px] bg-cover bg-center opacity-90"
        style={{
          backgroundImage: "url('https://cdn.poehali.dev/projects/b69e69c0-67e8-4990-8ea3-89b409ce2aa3/files/802d38fe-f182-4f47-a714-2aaa19552443.jpg')"
        }}
      />
      
      <div className="relative z-10 flex items-center justify-center min-h-screen">
        <h1 className="text-6xl md:text-8xl font-heading font-bold text-center animate-fade-in">
          Добро пожаловать<br />в Пит Стоп Бургер
        </h1>
      </div>
    </div>
  );
};

export default Index;
