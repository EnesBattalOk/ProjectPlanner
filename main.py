import os
from urllib.parse import urlparse
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', os.environ.get('SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bu sayfayı görüntülemek için giriş yapmalısınız.'
login_manager.login_message_category = 'error'


def is_safe_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return test_url.scheme in ('', 'http', 'https') and ref_url.netloc == test_url.netloc


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    title = db.Column(db.String(100), default='Developer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ideas = db.relationship('Idea', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Idea(db.Model):
    __tablename__ = 'ideas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    elevator_pitch = db.Column(db.Text)
    problem_statement = db.Column(db.Text)
    target_audience = db.Column(db.String(200))
    unique_value = db.Column(db.Text)
    tech_stack = db.Column(db.String(300))
    
    status = db.Column(db.String(20), default='draft')
    priority = db.Column(db.String(20), default='medium')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def status_color(self):
        colors = {
            'draft': 'gray',
            'reviewing': 'warning',
            'approved': 'success',
            'in_progress': 'primary',
            'completed': 'purple',
            'archived': 'gray'
        }
        return colors.get(self.status, 'gray')
    
    @property
    def status_label(self):
        labels = {
            'draft': 'Taslak',
            'reviewing': 'İnceleniyor',
            'approved': 'Onaylandı',
            'in_progress': 'Geliştiriliyor',
            'completed': 'Tamamlandı',
            'archived': 'Arşivlendi'
        }
        return labels.get(self.status, 'Taslak')
    
    @property
    def priority_color(self):
        colors = {
            'low': 'gray',
            'medium': 'warning',
            'high': 'danger'
        }
        return colors.get(self.priority, 'gray')
    
    @property
    def priority_label(self):
        labels = {
            'low': 'Düşük',
            'medium': 'Orta',
            'high': 'Yüksek'
        }
        return labels.get(self.priority, 'Orta')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')


@app.route('/dashboard')
@login_required
def dashboard():
    total_ideas = Idea.query.filter_by(user_id=current_user.id).count()
    active_ideas = Idea.query.filter_by(user_id=current_user.id, status='in_progress').count()
    recent_ideas = Idea.query.filter_by(user_id=current_user.id).order_by(Idea.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', 
                         total_ideas=total_ideas,
                         active_ideas=active_ideas,
                         pending_todos=0,
                         completed_count=Idea.query.filter_by(user_id=current_user.id, status='completed').count(),
                         recent_ideas=recent_ideas)


@app.route('/ideas')
@login_required
def ideas():
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    
    query = Idea.query.filter_by(user_id=current_user.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    
    ideas_list = query.order_by(Idea.updated_at.desc()).all()
    return render_template('ideas.html', ideas=ideas_list, 
                         status_filter=status_filter, 
                         priority_filter=priority_filter)


VALID_STATUSES = ['draft', 'reviewing', 'approved', 'in_progress', 'completed', 'archived']
VALID_PRIORITIES = ['low', 'medium', 'high']


@app.route('/ideas/new', methods=['GET', 'POST'])
@login_required
def new_idea():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        elevator_pitch = request.form.get('elevator_pitch', '').strip()
        problem_statement = request.form.get('problem_statement', '').strip()
        target_audience = request.form.get('target_audience', '').strip()
        unique_value = request.form.get('unique_value', '').strip()
        tech_stack = request.form.get('tech_stack', '').strip()
        status = request.form.get('status', 'draft')
        priority = request.form.get('priority', 'medium')
        
        if not title:
            flash('Fikir başlığı zorunludur.', 'error')
            return render_template('idea_form.html', idea=None)
        
        if status not in VALID_STATUSES:
            status = 'draft'
        if priority not in VALID_PRIORITIES:
            priority = 'medium'
        
        idea = Idea(
            user_id=current_user.id,
            title=title,
            elevator_pitch=elevator_pitch,
            problem_statement=problem_statement,
            target_audience=target_audience,
            unique_value=unique_value,
            tech_stack=tech_stack,
            status=status,
            priority=priority
        )
        
        db.session.add(idea)
        db.session.commit()
        
        flash('Fikir başarıyla eklendi!', 'success')
        return redirect(url_for('ideas'))
    
    return render_template('idea_form.html', idea=None)


@app.route('/ideas/<int:idea_id>')
@login_required
def view_idea(idea_id):
    idea = Idea.query.filter_by(id=idea_id, user_id=current_user.id).first_or_404()
    return render_template('idea_detail.html', idea=idea)


@app.route('/ideas/<int:idea_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_idea(idea_id):
    idea = Idea.query.filter_by(id=idea_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        
        if not title:
            flash('Fikir başlığı zorunludur.', 'error')
            return render_template('idea_form.html', idea=idea)
        
        status = request.form.get('status', 'draft')
        priority = request.form.get('priority', 'medium')
        
        if status not in VALID_STATUSES:
            status = idea.status
        if priority not in VALID_PRIORITIES:
            priority = idea.priority
        
        idea.title = title
        idea.elevator_pitch = request.form.get('elevator_pitch', '').strip()
        idea.problem_statement = request.form.get('problem_statement', '').strip()
        idea.target_audience = request.form.get('target_audience', '').strip()
        idea.unique_value = request.form.get('unique_value', '').strip()
        idea.tech_stack = request.form.get('tech_stack', '').strip()
        idea.status = status
        idea.priority = priority
        
        db.session.commit()
        
        flash('Fikir başarıyla güncellendi!', 'success')
        return redirect(url_for('view_idea', idea_id=idea.id))
    
    return render_template('idea_form.html', idea=idea)


@app.route('/ideas/<int:idea_id>/delete', methods=['POST'])
@login_required
def delete_idea(idea_id):
    idea = Idea.query.filter_by(id=idea_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(idea)
    db.session.commit()
    
    flash('Fikir başarıyla silindi.', 'success')
    return redirect(url_for('ideas'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        if not email or not password:
            flash('Lütfen tüm alanları doldurun.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                flash('Başarıyla giriş yaptınız!', 'success')
                return redirect(next_page)
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('E-posta veya şifre hatalı.', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not email or not password or not confirm_password:
            flash('Lütfen tüm alanları doldurun.', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Kullanıcı adı en az 3 karakter olmalıdır.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Şifre en az 6 karakter olmalıdır.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Şifreler eşleşmiyor.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Bu e-posta adresi zaten kullanılıyor.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanılıyor.', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Hesabınız oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)